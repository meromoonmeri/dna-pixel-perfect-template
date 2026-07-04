#!/usr/bin/env python3
"""Verify local references used by the Duet Night Abyss mirror.

This checks HTML/CSS/JS references that should exist in the repository. It ignores
optional MP3 files and intentionally external PV videos listed in OPTIONAL_*.txt.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXT = {".html", ".css", ".js", ".json", ".md", ".txt"}
ASSET_RE = r"(?:png|jpe?g|webp|gif|svg|ico|css|js|mp3|mp4|woff2?|ttf|otf)"
OPTIONAL = {
    "resource_assets/theme1-f0af692d.mp3",
    "resource_assets/BinaryFate-73f0c310.mp3",
    "resource_assets/theme0-5bdc16d3.mp3",
    "resource_assets/theme2-51179355.mp3",
    "resource_assets/theme3-22a27a7c.mp3",
    "resource_assets/theme4-e6c9ae53.mp3",
    "resource_assets/theme5-c33ecb9e.mp3",
}


def exists_root_ref(ref: str) -> bool:
    ref = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref or ref.startswith(("http://", "https://", "//", "data:", "mailto:")):
        return True
    if ref.startswith("./"):
        rel = ref[2:]
        if rel in OPTIONAL:
            return True
        return (ROOT / rel).exists()
    if ref.startswith("/"):
        return (ROOT / ref.lstrip("/")).exists()
    return True


def exists_relative(source: Path, ref: str) -> bool:
    ref = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref or ref.startswith(("http://", "https://", "//", "data:", "mailto:")):
        return True
    target = (source.parent / ref).resolve()
    try:
        rel = target.relative_to(ROOT).as_posix()
    except ValueError:
        return False
    if rel in OPTIONAL:
        return True
    return target.exists()


def main() -> int:
    missing: list[tuple[str, str]] = []
    for source in ROOT.rglob("*"):
        if not source.is_file() or source.suffix.lower() not in TEXT_EXT:
            continue
        if ".git" in source.parts or "node_modules" in source.parts:
            continue
        text = source.read_text(errors="ignore")
        rel_source = source.relative_to(ROOT).as_posix()

        if source.suffix.lower() == ".html":
            for ref in re.findall(r'(?:src|href)="([^"]+)"', text):
                if not exists_root_ref(ref):
                    missing.append((rel_source, ref))

        if source.suffix.lower() == ".css":
            for ref in re.findall(r"url\((?:\"|')?([^\"')]+)(?:\"|')?\)", text):
                if not exists_relative(source, ref):
                    missing.append((rel_source, ref))

        if source.suffix.lower() == ".js":
            for ref in re.findall(rf"[\"'](\./(?:imgs|font|js|videos|resource_assets)/[^\"']+?\.{ASSET_RE})[\"']", text):
                if not exists_root_ref(ref):
                    missing.append((rel_source, ref))
            for ref in re.findall(r"import\([\"'](\./[^\"']+?\.js)[\"']\)", text):
                if not exists_relative(source, ref):
                    missing.append((rel_source, ref))

    # Dynamic character/faction assets used by RolePage / RoleWeaponPage.
    protagonist = ROOT / "resource_assets" / "protagonist-158ba920.js"
    if protagonist.exists():
        text = protagonist.read_text(errors="ignore")
        ids = [m.group(2) for m in re.finditer(r'index:(\d+),id:"([^"]+)",name:e\("role\.([^.]+)\.name"\)', text)]
        for rid in ids:
            for ref in [
                f"imgs/role/pc/detail/role-{rid}.webp",
                f"imgs/role/pc/detail/bg-{rid}.webp",
                f"imgs/role/pc/detail/name-{rid}.webp",
                f"imgs/role/pc/detail/avatar-{rid}.webp",
                f"imgs/role/mobile/detail/role-{rid}.webp",
                f"imgs/role/mobile/detail/avatar-{rid}.webp",
            ]:
                if not (ROOT / ref).exists():
                    missing.append(("dynamic-role-assets", ref))
        for i in range(0, 7):
            for ref in [
                f"imgs/role/pc/detail/icon0{i}.png",
                f"imgs/role/mobile/icon0{i}.webp",
                f"imgs/role/mobile/role0{i}.webp",
            ]:
                if not (ROOT / ref).exists():
                    missing.append(("dynamic-faction-assets", ref))
        for i in range(1, 7):
            for ref in [f"imgs/role/pc/detail/icon{i}.png", f"imgs/role/pc/detail/0{i}.png"]:
                if not (ROOT / ref).exists():
                    missing.append(("dynamic-faction-assets", ref))

    # Weapon presentation videos used by the weapon overlay/player.
    store = ROOT / "resource_assets" / "store-2942ac35.js"
    if store.exists():
        text = store.read_text(errors="ignore")
        for ref in sorted(set(re.findall(r'"(/video/[^"]+\.mp4)"', text))):
            if not (ROOT / ref.lstrip("/")).exists():
                missing.append(("dynamic-weapon-video-assets", ref.lstrip("/")))

    if missing:
        print("Missing local references:")
        for src, ref in missing:
            print(f"- {src}: {ref}")
        return 1
    print("OK: all required local references exist, including all character/faction detail assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
