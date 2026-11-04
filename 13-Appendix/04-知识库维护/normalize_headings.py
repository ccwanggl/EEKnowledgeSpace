from __future__ import annotations

from pathlib import Path
import argparse
import re


VAULT = Path(__file__).resolve().parents[2]
EXCLUDED = {".obsidian", ".trash", "copilot", "Clippings", "Excalidraw"}
EXCLUDED_FILES = {"99-历史总索引归档.md", "修改摘要.md", "000-修改摘要.md"}
HEADING = re.compile(r"^(#{1,6})(\s+.*)$")


def is_content(path: Path) -> bool:
    return path.name not in EXCLUDED_FILES and not any(
        part in EXCLUDED for part in path.relative_to(VAULT).parts
    )


def normalize(text: str, include_jumps: bool = False) -> str:
    lines = text.splitlines(keepends=True)
    headings: list[tuple[int, int]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line.rstrip("\r\n"))
        if match:
            headings.append((index, len(match.group(1))))

    if not headings:
        return text

    first_level = headings[0][1]
    h1_count = sum(level == 1 for _, level in headings)
    if first_level == 1 and h1_count == 1 and not include_jumps:
        return text
    levels: dict[int, int] = {}

    if h1_count == 0:
        levels[headings[0][0]] = 1
        for index, level in headings[1:]:
            levels[index] = level
    elif h1_count > 1:
        first_index = headings[0][0]
        levels[first_index] = 1
        for index, level in headings[1:]:
            levels[index] = min(6, level + 1)
    else:
        for index, level in headings:
            levels[index] = level

    previous = 0
    for index, _ in headings:
        level = levels[index]
        if previous and level > previous + 1:
            level = previous + 1
            levels[index] = level
        previous = level

    for index, _ in headings:
        raw = lines[index]
        ending = "\r\n" if raw.endswith("\r\n") else "\n" if raw.endswith("\n") else ""
        body = raw.rstrip("\r\n")
        match = HEADING.match(body)
        assert match is not None
        lines[index] = f"{'#' * levels[index]}{match.group(2)}{ending}"
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--all-jumps", action="store_true")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in VAULT.rglob("*.md"):
        if not is_content(path):
            continue
        old = path.read_text(encoding="utf-8-sig")
        new = normalize(old, include_jumps=args.all_jumps)
        if new != old:
            changed.append(path)
            if args.apply:
                path.write_text(new, encoding="utf-8", newline="")

    action = "updated" if args.apply else "would update"
    print(f"{action}: {len(changed)} files")
    for path in changed[:30]:
        print(path.relative_to(VAULT).as_posix())
    if len(changed) > 30:
        print(f"... {len(changed) - 30} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
