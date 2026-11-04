from __future__ import annotations

from pathlib import Path
import argparse
import re


VAULT = Path(__file__).resolve().parents[2]
TOP_LEVEL = [
    "01-Foundations",
    "02-Analog-Electronics",
    "03-Digital-Electronics",
    "04-Microcontrollers",
    "05-Communication",
    "06-PCB-Design",
    "07-Power-Management",
    "08-Sensors-Actuators",
    "09-Debugging-Tools",
    "10-RTOS与系统",
    "11-Projects",
    "12-Resources",
    "13-Appendix",
]


def rel_without_suffix(path: Path) -> str:
    value = path.relative_to(VAULT).as_posix()
    return value[:-3] if value.lower().endswith(".md") else value


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
    parts = folder.name.split("-", 1)
    if len(parts) == 2:
        candidate = folder / f"{parts[0]}-{parts[1]}.md"
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    changed: list[Path] = []
    for name in TOP_LEVEL:
        folder = VAULT / name
        readme = folder / "00-README.md"
        if not readme.exists():
            continue
        old = readme.read_text(encoding="utf-8-sig")
        new = old.replace('WHERE file.name != "README"', 'WHERE file.name != "00-README"')
        if re.search(r"(?m)^## 模块导航\s*$", new):
            if new != old:
                changed.append(readme)
                if args.apply:
                    readme.write_text(new, encoding="utf-8", newline="")
            continue

        entries = []
        for child in sorted(path for path in folder.iterdir() if path.is_dir()):
            if child.name.lower() in {"assets", "scripts"}:
                continue
            target = landing_page(child)
            if target is None:
                continue
            display = child.name.split("-", 1)[-1]
            entries.append(f"- [[{rel_without_suffix(target)}|{display}]]")
        if not entries:
            continue

        section = "## 模块导航\n\n" + "\n".join(entries) + "\n\n---\n\n"
        marker = re.search(r"(?m)^## 本目录文件\s*$", new)
        if marker:
            new = new[: marker.start()] + section + new[marker.start() :]
        else:
            title = re.search(r"(?m)^#\s+.+$", new)
            if title is None:
                continue
            position = title.end()
            new = new[:position] + "\n\n" + section + new[position:].lstrip("\r\n")

        changed.append(readme)
        if args.apply:
            readme.write_text(new, encoding="utf-8", newline="")

    action = "updated" if args.apply else "would update"
    print(f"{action}: {len(changed)} files")
    for path in changed:
        print(path.relative_to(VAULT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
