from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

MAX_EXCERPT_CHARS = 800
RELOCATION_SCORE_FLOOR = 0.85
RELOCATION_SCORE_GAP = 0.20
DEFAULT_SAMPLE_RATE = 0.02


def normalize_source_uri(path: str | Path, repo_root: str | Path = ".") -> str:
    """Return a stable POSIX repo-relative source URI when possible."""
    root = Path(repo_root).resolve()
    candidate = Path(path)
    resolved = candidate if candidate.is_absolute() else root / candidate
    try:
        return resolved.resolve().relative_to(root).as_posix()
    except ValueError:
        return resolved.resolve().as_posix()


def compute_sha256(data: bytes | str) -> str:
    payload = data.encode("utf-8") if isinstance(data, str) else data
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def line_span_to_offsets(text: str, start_line: int, end_line: int) -> dict:
    if start_line < 1:
        raise ValueError("start_line must be 1 or greater")
    if end_line < start_line:
        raise ValueError("end_line must be greater than or equal to start_line")
    lines = text.splitlines(keepends=True)
    if not lines and start_line == 1 and end_line == 1:
        return {"start_line": 1, "end_line": 1, "start_byte": 0, "end_byte": 0}
    if end_line > len(lines):
        raise ValueError(f"line span {start_line}-{end_line} exceeds file length {len(lines)}")
    start_text = "".join(lines[: start_line - 1])
    span_text = "".join(lines[start_line - 1 : end_line])
    start_byte = len(start_text.encode("utf-8"))
    end_byte = start_byte + len(span_text.encode("utf-8"))
    return {
        "start_line": start_line,
        "end_line": end_line,
        "start_byte": start_byte,
        "end_byte": end_byte,
    }


def make_span_provenance(source_uri: str | Path, start_line: int, end_line: int, repo_root: str | Path = ".") -> dict:
    normalized = normalize_source_uri(source_uri, repo_root)
    path = _resolve_source_uri(normalized, repo_root)
    data = path.read_bytes()
    text = data.decode("utf-8")
    offsets = line_span_to_offsets(text, start_line, end_line)
    span_bytes = data[offsets["start_byte"] : offsets["end_byte"]]
    span_byte_length = len(span_bytes)
    span_line_count = end_line - start_line + 1
    excerpt = span_bytes.decode("utf-8", errors="replace")
    excerpt_truncated = len(excerpt) > MAX_EXCERPT_CHARS
    if len(excerpt) > MAX_EXCERPT_CHARS:
        excerpt = excerpt[:MAX_EXCERPT_CHARS] + "\n..."
    span_hash = compute_sha256(span_bytes)
    return {
        "source_uri": normalized,
        "start_line": offsets["start_line"],
        "end_line": offsets["end_line"],
        "start_byte": offsets["start_byte"],
        "end_byte": offsets["end_byte"],
        "span_byte_length": span_byte_length,
        "span_line_count": span_line_count,
        "hash_algorithm": "sha256",
        "span_hash": span_hash,
        "content_hash": compute_sha256(data),
        "prefix_hash": _adjacent_line_hash(data, start_line, before=True),
        "suffix_hash": _adjacent_line_hash(data, end_line, before=False),
        "section_anchor_hash": _section_anchor_hash(data, start_line),
        "occurrence_index": _occurrence_index(data, span_hash, span_byte_length, span_line_count, offsets["start_byte"]),
        "bounded_excerpt": excerpt,
        "excerpt_truncated": excerpt_truncated,
        "verified": True,
        "location_changed": False,
        "reason": "span hash generated",
    }


def verify_span_provenance(entry: dict[str, Any], repo_root: str | Path = ".", sample_rate: float = DEFAULT_SAMPLE_RATE) -> dict:
    source_uri = str(entry.get("source_uri", ""))
    expected_span_hash = entry.get("span_hash")
    result = {
        "result_status": "fail",
        "reason": "",
        "source_uri": source_uri,
        "expected_span_hash": expected_span_hash,
        "actual_span_hash": None,
        "location_changed": False,
        "winning_tier": "",
        "confidence": 0.0,
        "score_gap": 0.0,
        "candidate_count": 0,
        "sampled_reaudit": _should_sample_reaudit(entry, sample_rate),
        "sampled_reaudit_result": "not_sampled",
        "calibration_status": "not_calibrated",
    }
    if not source_uri:
        result["reason"] = "missing source_uri"
        _finalize_calibration(result, entry)
        return result
    if not expected_span_hash:
        result["reason"] = "missing span_hash"
        _finalize_calibration(result, entry)
        return result
    try:
        data = _resolve_source_uri(source_uri, repo_root).read_bytes()
        start_byte = int(entry["start_byte"])
        span_byte_length = int(entry.get("span_byte_length", int(entry["end_byte"]) - start_byte))
        original_span = data[start_byte : start_byte + span_byte_length]
    except Exception as exc:  # noqa: BLE001 - verifier must report, not crash.
        result["reason"] = str(exc)
        _finalize_calibration(result, entry)
        return result
    result["actual_span_hash"] = compute_sha256(original_span)
    if result["actual_span_hash"] != expected_span_hash:
        matches = _find_span_hash_matches(data, expected_span_hash, span_byte_length, int(entry.get("span_line_count", 1)))
        result["candidate_count"] = len(matches)
        if len(matches) == 1:
            result["result_status"] = "pass"
            result["reason"] = "pass_relocated_unique"
            result["actual_span_hash"] = expected_span_hash
            result["location_changed"] = True
            result["current_location"] = matches[0]
            result["winning_tier"] = "relocated_unique"
            result["confidence"] = 1.0
            _finalize_calibration(result, entry)
            return result
        if len(matches) > 1:
            scored = _score_relocation_candidates(data, matches, entry)
            winner = _select_relocation_winner(scored)
            result["relocation_candidates"] = scored
            if winner:
                result["result_status"] = "pass"
                result["reason"] = "pass_relocated_scored"
                result["actual_span_hash"] = expected_span_hash
                result["location_changed"] = True
                result["current_location"] = winner["location"]
                result["relocation_score"] = winner["score"]
                result["relocation_score_gap"] = winner["score_gap"]
                result["context_anchor_matched"] = True
                result["winning_tier"] = "relocated_scored"
                result["confidence"] = winner["score"]
                result["score_gap"] = winner["score_gap"]
                _finalize_calibration(result, entry)
                return result
            result["reason"] = "fail_ambiguous_force_reaudit"
            result["winning_tier"] = "ambiguous_force_reaudit"
            result["confidence"] = scored[0]["score"] if scored else 0.0
            result["score_gap"] = round(scored[0]["score"] - scored[1]["score"], 6) if len(scored) > 1 else 0.0
            _finalize_calibration(result, entry)
            return result
        result["reason"] = "fail_missing_force_reaudit"
        result["winning_tier"] = "missing_force_reaudit"
        _finalize_calibration(result, entry)
        return result
    result["result_status"] = "pass"
    result["reason"] = "pass_original_offset"
    result["winning_tier"] = "exact_offset"
    result["confidence"] = 1.0
    _finalize_calibration(result, entry)
    return result


def verify_provenance_entries(entries: list[Any], repo_root: str | Path = ".", require_span_hash: bool = True, sample_rate: float = DEFAULT_SAMPLE_RATE) -> dict:
    failures = []
    verifications = []
    legacy_count = 0
    for index, entry in enumerate(entries):
        if isinstance(entry, str):
            legacy_count += 1
            verifications.append({"index": index, "result_status": "legacy", "source_uri": entry})
            continue
        if not isinstance(entry, dict):
            failures.append({"index": index, "reason": "unsupported provenance entry type"})
            continue
        if entry.get("source_uri") and require_span_hash and not entry.get("span_hash"):
            failures.append({"index": index, "source_uri": entry.get("source_uri"), "reason": "missing span_hash"})
            continue
        if entry.get("source_uri") and entry.get("span_hash"):
            verified = verify_span_provenance(entry, repo_root=repo_root, sample_rate=sample_rate)
            verifications.append({"index": index, **verified})
            if verified["result_status"] != "pass":
                failures.append({"index": index, **verified})
        else:
            verifications.append({"index": index, "result_status": "skipped", "reason": "no source_uri"})
    return {
        "result_status": "fail" if failures else "pass",
        "require_span_hash": require_span_hash,
        "entries_total": len(entries),
        "verified_count": sum(1 for item in verifications if item.get("result_status") == "pass"),
        "legacy_count": legacy_count,
        "failures": failures,
        "verifications": verifications,
    }


def _resolve_source_uri(source_uri: str, repo_root: str | Path) -> Path:
    path = Path(source_uri)
    if path.is_absolute():
        return path
    return Path(repo_root).resolve() / path


def _find_span_hash_matches(data: bytes, expected_span_hash: str, span_byte_length: int, span_line_count: int) -> list[dict]:
    matches = []
    for start_line, start_byte in _line_starts(data):
        end_byte = start_byte + span_byte_length
        if end_byte > len(data):
            continue
        candidate = data[start_byte:end_byte]
        if _span_line_count(candidate) != span_line_count:
            continue
        if compute_sha256(candidate) != expected_span_hash:
            continue
        matches.append(
            {
                "start_line": start_line,
                "end_line": start_line + span_line_count - 1,
                "start_byte": start_byte,
                "end_byte": end_byte,
                "span_hash": expected_span_hash,
            }
        )
    return [
        {**match, "occurrence_index": index}
        for index, match in enumerate(sorted(matches, key=lambda item: item["start_byte"]))
    ]


def _line_starts(data: bytes) -> list[tuple[int, int]]:
    starts = [(1, 0)]
    line = 2
    for index, byte in enumerate(data):
        if byte == 10 and index + 1 < len(data):
            starts.append((line, index + 1))
            line += 1
    return starts


def _line_ranges(data: bytes) -> list[tuple[int, int, int]]:
    starts = _line_starts(data)
    ranges = []
    for index, (line, start) in enumerate(starts):
        end = starts[index + 1][1] if index + 1 < len(starts) else len(data)
        ranges.append((line, start, end))
    return ranges


def _span_line_count(span: bytes) -> int:
    if not span:
        return 1
    return span.count(b"\n") + (0 if span.endswith(b"\n") else 1)


def _adjacent_line_hash(data: bytes, line: int, before: bool) -> str | None:
    target_line = line - 1 if before else line + 1
    if target_line < 1:
        return None
    for current_line, start, end in _line_ranges(data):
        if current_line == target_line:
            return compute_sha256(data[start:end])
    return None


def _section_anchor_hash(data: bytes, start_line: int) -> str | None:
    anchor = None
    for line, start, end in _line_ranges(data):
        if line >= start_line:
            break
        text = data[start:end].decode("utf-8", errors="replace").strip()
        if text.startswith("#"):
            anchor = data[start:end]
    return compute_sha256(anchor) if anchor else None


def _occurrence_index(data: bytes, span_hash: str, span_byte_length: int, span_line_count: int, start_byte: int) -> int:
    for index, match in enumerate(_find_span_hash_matches(data, span_hash, span_byte_length, span_line_count)):
        if match["start_byte"] == start_byte:
            return index
    return 0


def _score_relocation_candidates(data: bytes, matches: list[dict], entry: dict[str, Any]) -> list[dict]:
    total_lines = max(len(_line_ranges(data)), 1)
    total_bytes = max(len(data), 1)
    original_line = int(entry.get("start_line", 1))
    original_byte = int(entry.get("start_byte", 0))
    scored = []
    for match in matches:
        prefix_matches = bool(entry.get("prefix_hash") and entry.get("prefix_hash") == _adjacent_line_hash(data, match["start_line"], before=True))
        suffix_matches = bool(entry.get("suffix_hash") and entry.get("suffix_hash") == _adjacent_line_hash(data, match["end_line"], before=False))
        section_matches = bool(entry.get("section_anchor_hash") and entry.get("section_anchor_hash") == _section_anchor_hash(data, match["start_line"]))
        occurrence_matches = entry.get("occurrence_index") == match.get("occurrence_index")
        line_proximity = max(0.0, 1.0 - (abs(match["start_line"] - original_line) / total_lines))
        byte_proximity = max(0.0, 1.0 - (abs(match["start_byte"] - original_byte) / total_bytes))
        score = (
            (0.30 if prefix_matches else 0.0)
            + (0.30 if suffix_matches else 0.0)
            + (0.25 if section_matches else 0.0)
            + (0.10 if occurrence_matches else 0.0)
            + (0.025 * line_proximity)
            + (0.025 * byte_proximity)
        )
        scored.append(
            {
                "location": {key: match[key] for key in ["start_line", "end_line", "start_byte", "end_byte"]},
                "occurrence_index": match.get("occurrence_index"),
                "score": round(score, 6),
                "prefix_hash_match": prefix_matches,
                "suffix_hash_match": suffix_matches,
                "section_anchor_hash_match": section_matches,
                "occurrence_index_match": occurrence_matches,
                "line_proximity": round(line_proximity, 6),
                "byte_proximity": round(byte_proximity, 6),
                "context_anchor_match": prefix_matches or suffix_matches or section_matches,
            }
        )
    return sorted(scored, key=lambda item: (-item["score"], item["location"]["start_byte"]))


def _select_relocation_winner(scored: list[dict]) -> dict | None:
    if not scored:
        return None
    top = scored[0]
    second_score = scored[1]["score"] if len(scored) > 1 else 0.0
    score_gap = round(top["score"] - second_score, 6)
    if top["score"] < RELOCATION_SCORE_FLOOR:
        return None
    if score_gap < RELOCATION_SCORE_GAP:
        return None
    if not top["context_anchor_match"]:
        return None
    return {**top, "score_gap": score_gap}


def _should_sample_reaudit(entry: dict[str, Any], sample_rate: float) -> bool:
    if sample_rate <= 0:
        return False
    if sample_rate >= 1:
        return True
    material = "|".join(str(entry.get(key, "")) for key in ["source_uri", "span_hash", "content_hash"])
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    bucket = int(digest[:16], 16) / float(0xFFFFFFFFFFFFFFFF)
    return bucket < sample_rate


def _finalize_calibration(result: dict, entry: dict[str, Any]) -> None:
    if result["sampled_reaudit"]:
        strict = _strict_reaudit_passes(result, entry)
        result["sampled_reaudit_result"] = "pass" if strict else "fail"
        if not strict and result["result_status"] == "pass":
            result["result_status"] = "fail"
            result["reason"] = "sampled_reaudit_failed_calibration"
        result["calibration_status"] = "sampled_pass" if strict else "sampled_fail"
    else:
        result["sampled_reaudit_result"] = "not_sampled"
        result["calibration_status"] = "not_sampled"


def _strict_reaudit_passes(result: dict, entry: dict[str, Any]) -> bool:
    if result["result_status"] != "pass":
        return False
    if result["winning_tier"] == "exact_offset":
        return True
    if result["winning_tier"] == "relocated_unique":
        return bool(entry.get("prefix_hash") or entry.get("suffix_hash") or entry.get("section_anchor_hash"))
    if result["winning_tier"] == "relocated_scored":
        return bool(result.get("context_anchor_matched")) and result.get("confidence", 0.0) >= RELOCATION_SCORE_FLOOR
    return False
