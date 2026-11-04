from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import argparse
import re


VAULT = Path(__file__).resolve().parents[2]
EXCLUDED = {".obsidian", ".trash", "copilot", "Clippings", "Excalidraw"}
EXCLUDED_FILES = {"99-历史总索引归档.md", "修改摘要.md", "000-修改摘要.md"}
WIKI = re.compile(r"(?<!!)\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]")


def is_content(path: Path) -> bool:
    return path.name not in EXCLUDED_FILES and not any(
        part in EXCLUDED for part in path.relative_to(VAULT).parts
    )


def rel(path: Path) -> str:
    return path.relative_to(VAULT).as_posix()


def landing_page(folder: Path) -> Path | None:
    for name in ("00-README.md", "000-README.md"):
        candidate = folder / name
        if candidate.exists():
            return candidate
    overview = sorted(folder.glob("000-*.md"))
    if overview:
        return overview[0]
    direct = folder / f"{folder.name}.md"
    if direct.exists():
        return direct
    numbered_direct = folder / f"{folder.name.split('-', 1)[0]}-{folder.name.split('-', 1)[-1]}.md"
    if numbered_direct.exists():
        return numbered_direct
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    notes = [path for path in VAULT.rglob("*.md") if is_content(path)]
    by_relative = {rel(path).lower(): path for path in notes}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    directories: dict[str, list[Path]] = defaultdict(list)
    for path in notes:
        by_stem[path.stem.lower()].append(path)
    for path in VAULT.rglob("*"):
        if path.is_dir() and is_content(path):
            directories[path.name.lower()].append(path)

    changed_files: list[Path] = []
    replacement_count = 0
    reasons: Counter[str] = Counter()

    for source in notes:
        old = source.read_text(encoding="utf-8-sig")
        lines = old.splitlines(keepends=True)
        in_fence = False
        changed = False

        def replace(match: re.Match[str]) -> str:
            nonlocal replacement_count, changed
            raw = match.group(1).strip().replace("\\", "/")
            heading = match.group(2) or ""
            alias = match.group(3)
            lowered = raw.lower()
            target: Path | None = None
            default_alias = raw

            if lowered == "00-readme":
                target = VAULT / "00-Index" / "00-README.md"
                default_alias = "知识库首页"
                reason = "homepage"
            elif lowered == "002-时域分析":
                if rel(source).startswith("15-双控（控制理论与控制工程）/"):
                    target = VAULT / "15-双控（控制理论与控制工程）" / "02-经典控制理论" / "002-时域分析.md"
                else:
                    target = VAULT / "01-Foundations" / "05-信号与系统" / "002-时域响应与微分方程.md"
                reason = "time-domain"
            elif "/" not in raw:
                global_hits = by_stem.get(lowered, [])
                local = [path for path in global_hits if path.parent == source.parent]
                if len(global_hits) > 1 and len(local) == 1:
                    target = local[0]
                    reason = "local-ambiguous"

            if target is None:
                explicit_keys = (lowered, f"{lowered}.md")
                if any(key in by_relative for key in explicit_keys):
                    return match.group(0)
                if "/" not in raw and len(by_stem.get(lowered, [])) == 1:
                    return match.group(0)

            if target is None:
                folder_hits: list[Path] = []
                if "/" in raw:
                    candidate = VAULT / raw
                    if candidate.is_dir():
                        folder_hits = [candidate]
                else:
                    folder_hits = directories.get(lowered, [])
                if len(folder_hits) == 1:
                    target = landing_page(folder_hits[0])
                    if target is not None:
                        reason = "directory"

            if target is None:
                return match.group(0)

            key = rel(target)
            if key.lower().endswith(".md"):
                key = key[:-3]
            display = alias or default_alias
            replacement_count += 1
            reasons[reason] += 1
            changed = True
            return f"[[{key}{heading}|{display}]]"

        for index, line in enumerate(lines):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                lines[index] = WIKI.sub(replace, line)

        new = "".join(lines)
        if changed and new != old:
            changed_files.append(source)
            if args.apply:
                source.write_text(new, encoding="utf-8", newline="")

    action = "updated" if args.apply else "would update"
    print(f"{action}: {len(changed_files)} files, {replacement_count} links")
    print("reasons:", ", ".join(f"{key}={value}" for key, value in reasons.items()))
    for path in changed_files[:30]:
        print(rel(path))
    if len(changed_files) > 30:
        print(f"... {len(changed_files) - 30} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
