# QA checklist — Duet Night Abyss template

## Black-screen fix

- `index.html` now loads `resource_assets/app.bundle.js` as a classic browser script instead of relying on ESM module loading.
- This avoids the sandbox/CORS problem that can make the Arena preview stay black.
- The original ESM entry is preserved as `index.module.html`.

## Routes/pages present

The original router routes are present in the bundle:

- `#/home` — home / launch page
- `#/role_weapon` — characters & weapons
- `#/role` — character detail/mobile route
- `#/weapon` — weapon detail/mobile route
- `#/feature` — info/gameplay
- `#/worldview` — Atlasia/world/story/factions area
- `#/story` — local alias redirecting to `#/worldview`
- `#/news` — news landing
- `#/news/list` — news list
- `#/news/detail` — news detail
- `/news/content` — standalone content route from original bundle

`TOP-UP` is not an internal rendered route in the captured official bundle; it remains an outbound link to the official store, matching the original behavior.

## Characters/factions coverage

All role/faction visual assets referenced by the official Characters routes are included locally.

Factions:

- Protagonist
- Noctoyager
- Hyperborean Empire
- The Elysian Church
- Republic of Luca
- Huaxu
- No Affiliation

Characters:

- Berenica (`blnk`)
- Outsider (`atsd`)
- Sibylle (`xbe`)
- Lynn (`le`)
- Rhythm (`ls`)
- Daphne (`dfn`)
- Randy (`ld`)
- Hellfire (`hef`)
- Truffle and Filbert / Filbert (`slyzz`)
- Lisbell (`lzbe`)
- Rebecca (`lbk`)
- Tabethe (`tbs`)
- Zhiliu (`zl`)
- Fushu (`fs`)
- Psyche (`sq`)
- Fina (`fn`)
- Phantasio (`hj`)
- Nifle (`nfefr`)
- Margie (`mej`)
- Yale (`yeyalf`)
- Kezhou (`kz`)
- Yuming (`ym`)
- Suyi (`sy`)
- Camilla (`kml`)
- Flora (`flora`)
- Hilda (`hilda`)

## Local assets

- Required images, CSS, JS, fonts, character detail images, faction emblems, and local videos are included.
- `videos/trailer.mp4` is bundled locally.
- News background video is omitted to keep size low; the official poster image is local. Optional URL: `OPTIONAL_NEWS_BG_VIDEO.txt`.
- Music MP3 files are intentionally optional to keep repository size reasonable; restore them with `python3 download_optional_audio.py`.
- Character CV MP3 files are not bundled by default; the visual character/faction pages are complete.
- Weapon presentation videos are bundled locally in `video/pc/`.
- Huge PV videos are intentionally not bundled; see `OPTIONAL_LARGE_VIDEOS.txt`.

## Verification commands

Run from the repository root:

```bash
python3 scripts/verify_assets.py
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080/#/home
http://localhost:8080/#/role_weapon
http://localhost:8080/#/feature
http://localhost:8080/#/worldview
http://localhost:8080/#/story
http://localhost:8080/#/news
```

## Current automated check

`python3 scripts/verify_assets.py` passes: all required local references exist.

## Pixel/frame-perfect status

The implementation keeps the official Vue bundle, official CSS, fonts, images and layout assets. The only changes are infrastructure-level changes needed for local/sandbox rendering:

1. CDN paths rewritten to local repository paths.
2. ESM app re-bundled into a classic script for preview compatibility.
3. Analytics/captcha disabled/stubbed.
4. News API given a local fallback to avoid network blocking in sandbox previews.
5. Optional heavy audio/PV files excluded or restorable.
