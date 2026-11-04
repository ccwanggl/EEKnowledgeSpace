from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import sys


VAULT = Path(__file__).resolve().parents[2]
EXCLUDED_DIRS = {".obsidian", ".trash", "copilot", "Clippings", "Excalidraw"}
PYTHON_LANGUAGES = {"python", "py", "python3"}


@dataclass(frozen=True)
class CodeBlock:
    path: Path
    line: int
    language: str
    source: str


def is_content(path: Path) -> bool:
    return not any(part in EXCLUDED_DIRS for part in path.relative_to(VAULT).parts)


def iter_code_blocks(path: Path) -> list[CodeBlock]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    blocks: list[CodeBlock] = []
    index = 0

    while index < len(lines):
        line = lines[index].lstrip()
        if not line.startswith("```"):
            index += 1
            continue

        info = line[3:].strip().split(maxsplit=1)
        language = info[0].lower() if info else ""
        start = index + 2
        index += 1
        body: list[str] = []
        while index < len(lines) and not lines[index].lstrip().startswith("```"):
            body.append(lines[index])
            index += 1
        blocks.append(CodeBlock(path, start, language, "\n".join(body)))
        index += 1

    return blocks


def main() -> int:
    checked = 0
    failures: list[tuple[CodeBlock, SyntaxError]] = []

    for path in VAULT.rglob("*.md"):
        if not is_content(path):
            continue
        for block in iter_code_blocks(path):
            if block.language not in PYTHON_LANGUAGES:
                continue
            checked += 1
            try:
                ast.parse(block.source, filename=str(block.path))
            except SyntaxError as error:
                failures.append((block, error))

    print(f"python blocks checked: {checked}")
    print(f"syntax failures: {len(failures)}")
    for block, error in failures:
        relative = block.path.relative_to(VAULT).as_posix()
        source_line = block.line + (error.lineno or 1) - 1
        print(f"  {relative}:{source_line}: {error.msg}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
