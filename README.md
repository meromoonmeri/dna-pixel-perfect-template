# Duet Night Abyss — local front-end template

Local mirror generated from the supplied HTML/live static bundles.

## Run

Open it through a local web server for correct relative asset loading:

```bash
cd duet-night-abyss-template
python3 -m http.server 8080
# then open http://localhost:8080/#/home
# story/world/factions page:
http://localhost:8080/#/worldview
# alias also supported:
http://localhost:8080/#/story
```

## Notes

- CDN asset URLs were rewritten to local paths.
- `index.html` uses `resource_assets/app.bundle.js`, a non-module browser bundle, to avoid the black-screen issue in sandboxed previews. The original module entry is preserved as `index.module.html`.
- Tracking/captcha scripts were removed/stubbed for a standalone template.
- External store/social/API links remain as outbound links; news API has a small local fallback (`local-news-list.json`, `local-news-detail.json`).
- Trailer video is stored at `videos/trailer.mp4`; News background video at `videos/news-bg.mp4`.
- Music MP3 files are optional to keep the workspace under size limits; run `python3 download_optional_audio.py` to restore them locally.
- Story alias: `#/story` and `/story.html` redirect to the official `#/worldview` Atlasia/story/factions page.
- All Characters/Weapons route visual assets are included, including all factions and all character detail images such as Flora, Hilda, Fina, etc.
- Weapon presentation videos are bundled locally in `video/pc/` for the weapon overlay/player.
- Asset manifest: `ASSET_MANIFEST.tsv`.
- Total local payload at generation time: 279.4 MB.


Large PV videos are listed in `OPTIONAL_LARGE_VIDEOS.txt` (not bundled due size).

## Publish to GitHub

Preferred token-safe command from this folder:

```bash
GITHUB_TOKEN=YOUR_TEMP_TOKEN python3 scripts/publish_github.py --repo dna-pixel-perfect-template --public
```

The script reads the token from the environment, creates the repo, pushes `main`, then resets the remote URL so the token is not stored in `.git/config`.
