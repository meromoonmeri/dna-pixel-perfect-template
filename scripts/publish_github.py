#!/usr/bin/env python3
"""Create a GitHub repository and push this template.

Usage:
  GITHUB_TOKEN=YOUR_TEMP_TOKEN python3 scripts/publish_github.py --repo dna-pixel-perfect-template --public

The script reads the token from the environment and masks it in logs.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def redact(text: str) -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        text = text.replace(token, "***")
    text = re.sub(r"x-access-token:[^@\s]+@", "x-access-token:***@", text)
    text = re.sub(r"Authorization: Bearer [^\s]+", "Authorization: Bearer ***", text)
    return text


def api(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "arena-duet-template-publisher",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise SystemExit(redact(f"GitHub API error {e.code}: {body}")) from e


def run(cmd: list[str], quiet: bool = False) -> None:
    printable = redact(" ".join(cmd))
    print("$", printable)
    if quiet:
        res = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        res = subprocess.run(cmd, cwd=ROOT, text=True)
    if res.returncode != 0:
        if quiet:
            if res.stdout:
                print(redact(res.stdout))
            if res.stderr:
                print(redact(res.stderr))
        raise SystemExit(f"Command failed ({res.returncode}): {printable}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="dna-pixel-perfect-template")
    parser.add_argument("--public", action="store_true")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--description", default="Pixel-perfect static template for Duet Night Abyss official site UI")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Missing GITHUB_TOKEN environment variable")
    private = bool(args.private) and not args.public

    user = api("GET", "https://api.github.com/user", token)
    owner = user["login"]
    print(f"Authenticated as {owner}")

    try:
        repo = api(
            "POST",
            "https://api.github.com/user/repos",
            token,
            {
                "name": args.repo,
                "description": args.description,
                "private": private,
                "has_issues": True,
                "has_projects": False,
                "has_wiki": False,
            },
        )
    except SystemExit as exc:
        if "already exists" not in str(exc) and "name already exists" not in str(exc):
            raise
        repo = api("GET", f"https://api.github.com/repos/{owner}/{args.repo}", token)

    clone_url = repo["clone_url"]
    token_url = clone_url.replace("https://", f"https://x-access-token:{token}@")

    if not (ROOT / ".git").exists():
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
        run(["git", "config", "user.name", "Arena Agent"])
        run(["git", "config", "user.email", "agent@arena.local"])

    run(["git", "add", "."])
    subprocess.run(["git", "commit", "-q", "-m", "Initial Duet Night Abyss static template"], cwd=ROOT)
    subprocess.run(["git", "remote", "remove", "origin"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run(["git", "remote", "add", "origin", token_url])
    try:
        run(["git", "push", "--quiet", "--force", "-u", "origin", "main"], quiet=True)
    finally:
        subprocess.run(["git", "remote", "set-url", "origin", clone_url], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Published:", repo["html_url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
