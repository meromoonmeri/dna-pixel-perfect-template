#!/usr/bin/env python3
"""Download all character/faction visual assets referenced by the official role pages."""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://cdnstatic.herogame.com/static/duetnightabyss_gw_1_4"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
    "Referer": "https://duetnightabyss.dna-panstudio.com/",
})


def role_ids() -> list[str]:
    text = (ROOT / "resource_assets" / "protagonist-158ba920.js").read_text(errors="ignore")
    items = []
    for m in re.finditer(r'index:(\d+),id:"([^"]+)",name:e\("role\.([^.]+)\.name"\)', text):
        items.append((int(m.group(1)), m.group(2), m.group(3)))
    items.sort()
    return [i[1] for i in items]


def download(path: str) -> bool:
    out = ROOT / path.lstrip("/")
    if out.exists() and out.stat().st_size > 100:
        return True
    out.parent.mkdir(parents=True, exist_ok=True)
    url = BASE + path
    try:
        r = SESSION.get(url, timeout=30)
        if r.status_code != 200:
            print(f"MISS {r.status_code} {path}")
            return False
        out.write_bytes(r.content)
        print(f"OK {len(r.content):>8} {path}")
        time.sleep(0.02)
        return True
    except Exception as exc:
        print(f"ERR {path}: {exc}")
        return False


def main() -> int:
    ids = role_ids()
    paths: list[str] = []

    for rid in ids:
        paths += [
            f"/imgs/role/pc/detail/role-{rid}.webp",
            f"/imgs/role/pc/detail/bg-{rid}.webp",
            f"/imgs/role/pc/detail/name-{rid}.webp",
            f"/imgs/role/pc/detail/avatar-{rid}.webp",
            f"/imgs/role/mobile/detail/role-{rid}.webp",
            f"/imgs/role/mobile/detail/avatar-{rid}.webp",
        ]

    for i in range(1, 7):
        paths += [
            f"/imgs/role/pc/detail/0{i}.png",
            f"/imgs/role/pc/detail/icon{i}.png",
            f"/imgs/role/mobile/detail/icon0{i}.png",
        ]
    paths += ["/imgs/role/mobile/icon00.png", "/imgs/role/mobile/detail/plate.webp"]

    ok = 0
    for p in sorted(set(paths)):
        ok += int(download(p))

    # The mobile detail component references zero-padded pc/detail icon00..icon06,
    # but the CDN publishes pc/detail icon1..icon6. Create local compatibility aliases.
    detail = ROOT / "imgs" / "role" / "pc" / "detail"
    mobile = ROOT / "imgs" / "role" / "mobile"
    if (mobile / "icon00.png").exists() and not (detail / "icon00.png").exists():
        shutil.copy2(mobile / "icon00.png", detail / "icon00.png")
        print("ALIAS imgs/role/pc/detail/icon00.png")
    for i in range(1, 7):
        src = detail / f"icon{i}.png"
        dst = detail / f"icon0{i}.png"
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"ALIAS imgs/role/pc/detail/icon0{i}.png")

    print(f"Done: {ok}/{len(set(paths))} fetched/existing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
