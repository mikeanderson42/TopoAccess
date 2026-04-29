from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class FileFingerprint:
    path: str
    size: int
    mtime_ns: int
    sha256_prefix: str | None = None


@dataclass(frozen=True)
class SpanRequest:
    path: str | Path
    snippet: str
    max_scan_bytes: int = 2_000_000


@dataclass(frozen=True)
class SpanMatch:
    matched: bool
    path: str
    start_line: int | None = None
    end_line: int | None = None
    reason: str = ""
    bytes_scanned: int = 0


class ProvenanceFileCache:
    def __init__(self) -> None:
        self._cache: dict[tuple[str, int, int], str] = {}

    def get_text(self, path: str | Path, max_bytes: int = 2_000_000) -> str | None:
        p = Path(path)
        try:
            stat = p.stat()
        except OSError:
            return None
        if stat.st_size > max_bytes or _looks_binary(p):
            return None
        key = (str(p.resolve()), stat.st_size, stat.st_mtime_ns)
        if key not in self._cache:
            try:
                self._cache[key] = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                return None
        return self._cache[key]

    def find_span(self, path: str | Path, snippet: str, *, max_scan_bytes: int = 2_000_000) -> SpanMatch:
        if not snippet:
            return SpanMatch(False, str(path), reason="empty_snippet")
        text = self.get_text(path, max_scan_bytes)
        if text is None:
            return SpanMatch(False, str(path), reason="unreadable_or_too_large")
        position = text.find(snippet)
        if position < 0:
            return SpanMatch(False, str(path), reason="span_not_found", bytes_scanned=len(text.encode("utf-8")))
        start_line = text.count("\n", 0, position) + 1
        end_line = start_line + snippet.count("\n")
        return SpanMatch(True, str(path), start_line=start_line, end_line=end_line, reason="matched", bytes_scanned=len(text.encode("utf-8")))

    def fingerprint(self, path: str | Path, *, hash_prefix_bytes: int = 4096) -> FileFingerprint | None:
        p = Path(path)
        try:
            stat = p.stat()
            prefix = p.read_bytes()[:hash_prefix_bytes]
        except OSError:
            return None
        return FileFingerprint(str(p), stat.st_size, stat.st_mtime_ns, hashlib.sha256(prefix).hexdigest()[:16])


def verify_spans_batch(spans: Iterable[SpanRequest], cache: ProvenanceFileCache | None = None) -> list[SpanMatch]:
    index = cache or ProvenanceFileCache()
    return [index.find_span(span.path, span.snippet, max_scan_bytes=span.max_scan_bytes) for span in spans]


def _looks_binary(path: Path) -> bool:
    try:
        with path.open("rb") as stream:
            sample = stream.read(2048)
    except OSError:
        return True
    return b"\0" in sample
