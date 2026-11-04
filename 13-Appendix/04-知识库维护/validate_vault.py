from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote
import os
import re
import sys


VAULT = Path(__file__).resolve().parents[2]
DETAIL_LIMIT = int(os.environ.get("VAULT_VALIDATE_LIMIT", "20"))
EXCLUDED = {".obsidian", ".trash", "copilot", "Clippings", "Excalidraw"}
EXCLUDED_FILES = {"99-历史总索引归档.md", "修改摘要.md", "000-修改摘要.md"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".pdf"}

WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
OBSIDIAN_EMBED = re.compile(r"!\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\)")


def is_content(path: Path) -> bool:
    return path.name not in EXCLUDED_FILES and not any(
        part in EXCLUDED for part in path.relative_to(VAULT).parts
    )


def prose_only(text: str) -> str:
    text = re.sub(r"(?ms)^```.*?^```\s*", "", text)
    return re.sub(r"`[^`\n]+`", "", text)


def rel(path: Path) -> str:
    return path.relative_to(VAULT).as_posix()


def main() -> int:
    all_notes = [
        path
        for path in VAULT.rglob("*.md")
        if not any(part in EXCLUDED for part in path.relative_to(VAULT).parts)
    ]
    notes = [path for path in all_notes if is_content(path)]
    texts = {path: path.read_text(encoding="utf-8-sig") for path in notes}

    by_relative = {rel(path).lower(): path for path in all_notes}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_filename: dict[str, list[Path]] = defaultdict(list)
    for path in all_notes:
        by_stem[path.stem.lower()].append(path)
        by_filename[path.name.lower()].append(path)

    directories: dict[str, list[Path]] = defaultdict(list)
    for path in VAULT.rglob("*"):
        if path.is_dir() and is_content(path):
            directories[path.name.lower()].append(path)

    missing_links: list[tuple[Path, str]] = []
    ambiguous_links: list[tuple[Path, str]] = []
    directory_links: list[tuple[Path, str]] = []

    for source, text in texts.items():
        for match in WIKI_LINK.finditer(prose_only(text)):
            raw = match.group(1).strip().replace("\\", "/")
            lowered = raw.lower()
            hits: list[Path] = []

            for key in (lowered, f"{lowered}.md"):
                if key in by_relative:
                    hits = [by_relative[key]]
                    break

            if not hits and "/" in raw:
                candidate = source.parent / raw
                candidates = [candidate] if candidate.suffix.lower() == ".md" else [candidate, candidate.with_suffix(".md")]
                for item in candidates:
                    try:
                        key = item.resolve().relative_to(VAULT).as_posix().lower()
                    except ValueError:
                        continue
                    if key in by_relative:
                        hits = [by_relative[key]]
                        break

            if not hits:
                hits = by_filename.get(f"{Path(raw).name}.md".lower(), [])

            if not hits and "/" not in raw:
                stem = Path(raw).stem.lower() if lowered.endswith(".md") else lowered
                local = [path for path in by_stem.get(stem, []) if path.parent == source.parent]
                hits = local or by_stem.get(stem, [])

            if not hits:
                folder_hits: list[Path] = []
                if "/" in raw:
                    candidate = VAULT / raw
                    if candidate.is_dir():
                        folder_hits = [candidate]
                else:
                    folder_hits = directories.get(lowered, [])
                if len(folder_hits) == 1:
                    directory_links.append((source, raw))
                    continue

            if not hits:
                missing_links.append((source, raw))
            elif len(hits) > 1:
                ambiguous_links.append((source, raw))

    assets = [path for path in VAULT.rglob("*") if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES]
    assets_by_name: dict[str, list[Path]] = defaultdict(list)
    for path in assets:
        assets_by_name[path.name.lower()].append(path)

    missing_images: list[tuple[Path, str]] = []
    for source, text in texts.items():
        raw_references = [match.group(1).strip() for match in OBSIDIAN_EMBED.finditer(text)]
        raw_references.extend((match.group(1) or match.group(2)).strip() for match in MARKDOWN_IMAGE.finditer(text))
        for raw in raw_references:
            raw = unquote(raw).replace("\\", "/")
            if re.match(r"^(https?:|data:|app:)", raw, re.IGNORECASE):
                continue
            if not Path(raw).suffix:
                continue
            candidates = [source.parent / raw, VAULT / raw]
            if any(candidate.exists() for candidate in candidates):
                continue
            if len(assets_by_name.get(Path(raw).name.lower(), [])) != 1:
                missing_images.append((source, raw))

    odd_code: list[Path] = []
    odd_math: list[Path] = []
    no_h1: list[Path] = []
    multiple_h1: list[Path] = []
    heading_jumps: list[tuple[Path, int, int, int]] = []

    for path, text in texts.items():
        if len(re.findall(r"(?m)^```", text)) % 2:
            odd_code.append(path)
        if len(re.findall(r"\$\$", prose_only(text))) % 2:
            odd_math.append(path)

        clean = prose_only(text)
        headings = []
        for line_number, line in enumerate(clean.splitlines(), 1):
            match = re.match(r"^(#{1,6})\s+", line)
            if match:
                headings.append((line_number, len(match.group(1))))
        h1_count = sum(level == 1 for _, level in headings)
        if h1_count == 0:
            no_h1.append(path)
        elif h1_count > 1:
            multiple_h1.append(path)
        for (_, previous), (line_number, current) in zip(headings, headings[1:]):
            if current > previous + 1:
                heading_jumps.append((path, line_number, previous, current))

    sections = {
        "missing links": [(rel(path), value) for path, value in missing_links],
        "directory links": [(rel(path), value) for path, value in directory_links],
        "ambiguous links": [(rel(path), value) for path, value in ambiguous_links],
        "missing images": [(rel(path), value) for path, value in missing_images],
        "odd code fences": [rel(path) for path in odd_code],
        "odd math markers": [rel(path) for path in odd_math],
        "missing H1": [rel(path) for path in no_h1],
        "multiple H1": [rel(path) for path in multiple_h1],
        "heading jumps": [(rel(path), line, old, new) for path, line, old, new in heading_jumps],
    }

    print(f"notes: {len(notes)}")
    for name, values in sections.items():
        print(f"{name}: {len(values)}")
        for value in values[:DETAIL_LIMIT]:
            print(f"  {value}")
        if len(values) > DETAIL_LIMIT:
            print(f"  ... {len(values) - DETAIL_LIMIT} more")

    advisory = {"heading jumps"}
    hard_errors = sum(
        len(values) for name, values in sections.items() if name not in advisory
    )
    return 1 if hard_errors else 0


if __name__ == "__main__":
    sys.exit(main())
