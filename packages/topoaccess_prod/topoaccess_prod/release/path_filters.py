from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
}

BINARY_EXTENSIONS = {
    ".bin",
    ".exe",
    ".dll",
    ".dylib",
    ".so",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".tgz",
    ".pyc",
    ".pyo",
}


def iter_files(
    roots: Iterable[str | Path],
    *,
    exclude_dirs: Iterable[str] | None = None,
    max_file_bytes: int | None = None,
    extensions: set[str] | None = None,
    follow_symlinks: bool = False,
) -> Iterator[tuple[Path, dict]]:
    excluded = set(exclude_dirs or [])
    for root in roots:
        base = Path(root)
        if not base.exists():
            yield base, {"result_status": "error", "error_type": "missing_root", "path": str(base)}
            continue
        if base.is_file():
            yield from _yield_file(base, max_file_bytes=max_file_bytes, extensions=extensions)
            continue
        stack = [base]
        while stack:
            current = stack.pop()
            try:
                children = list(current.iterdir())
            except OSError as exc:
                yield current, {"result_status": "error", "error_type": type(exc).__name__, "path": str(current), "message": str(exc)}
                continue
            for child in children:
                if child.is_symlink() and not follow_symlinks:
                    yield child, {"result_status": "skipped", "skipped_reason": "symlink", "path": str(child)}
                    continue
                if child.is_dir():
                    if child.name in excluded or _matches_excluded_path(child, excluded):
                        continue
                    stack.append(child)
                    continue
                yield from _yield_file(child, max_file_bytes=max_file_bytes, extensions=extensions)


def _yield_file(path: Path, *, max_file_bytes: int | None, extensions: set[str] | None) -> Iterator[tuple[Path, dict]]:
    try:
        if extensions is not None and path.suffix.lower() not in extensions:
            yield path, {"result_status": "skipped", "skipped_reason": "extension", "path": str(path)}
            return
        size = path.stat().st_size
        if max_file_bytes is not None and size > max_file_bytes:
            yield path, {"result_status": "skipped", "skipped_reason": "too_large", "path": str(path), "bytes": size}
            return
        yield path, {"result_status": "candidate", "path": str(path), "bytes": size}
    except OSError as exc:
        yield path, {"result_status": "error", "error_type": type(exc).__name__, "path": str(path), "message": str(exc)}


def _matches_excluded_path(path: Path, excluded: set[str]) -> bool:
    as_posix = path.as_posix()
    return any(pattern in as_posix for pattern in excluded if "/" in pattern)
