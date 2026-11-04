"""Blocks anything that must never reach GitHub: screenshots and images, meeting transcripts and recordings, chat
logs, data exports, office originals and secrets. Runs as pre-commit (staged files) and pre-push (every file the
pushed commits add or change), so a commit made with --no-verify is still stopped at the push.

A file that is genuinely safe (a diagram we drew, a test fixture) goes in .githooks/allow.txt, one glob per line,
added on purpose. Files already on GitHub are only checked again when they change.

Private ids (tenant, app, object, subscription, Anthropic ids) are read at check time from the repo's own .env and
from any file listed in .git/info/id-sources (one path per line, never committed), so the check itself never holds
an id. A GUID is also caught by its first 8 characters. Ids are blocked everywhere, allow list or not.
Standing rule, Udbhav 2026-10-29, after the 2026-10-07 real-data screenshot.
"""
from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import Path

BLOCKED = [
    (r"(^|/)Meeting Transcripts/(?!README\.md$)", "meeting transcript"),
    (r"(^|/)exports/", "exports folder (real system data)"),
    (r"(^|/)(fixtures/raw|out|raw)/", "raw or run output data"),
    (r"_RAW[._]", "verbatim RAW copy"),
    (r"\.(png|jpe?g|gif|webp|heic|bmp|tiff?)$", "image or screenshot"),
    (r"\.(vtt|srt|mp4|m4a|mp3|wav|mov|webm)$", "recording or caption file"),
    (r"\.(jsonl|eml|msg)$", "chat log or email"),
    (r"\.(csv|xlsx?|pdf|docx?|pptx?|zip)$", "export, office original or document"),
    (r"(^|/)\.env$", "secrets file"),
]
SECRETS = [
    (rb"sk-ant-(api|oat|admin)\d*-[A-Za-z0-9_-]{20,}", "Anthropic key or token"),
    (rb"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}", "signed-in token (JWT)"),
    (rb"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (rb"[A-Za-z0-9_~.-]{3}8Q~[A-Za-z0-9_~.-]{31,}", "Entra client secret"),
    (rb"(?i)(client_secret|api_key|password)[ \t]*[=:][ \t]*[\"']?[A-Za-z0-9_~.+/-]{16,}", "secret value"),
]
ZERO = "0" * 40


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


ID_KEY = re.compile(r"(ID|AUDIENCE|TENANT|SECRET|KEY|TOKEN|PASSWORD)$", re.I)
GUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def private_values(root: Path) -> list[bytes]:
    """Values of id and secret settings in the local .env files, to be found in no committed file."""
    sources = [root / ".env"]
    extra = root / ".git" / "info" / "id-sources"
    if extra.exists():
        sources += [Path(s.strip()) for s in extra.read_text(encoding="utf-8").splitlines() if s.strip()]
    vals: set[str] = set()
    for src in sources:
        if not src.exists():
            continue
        for line in src.read_text(encoding="utf-8", errors="ignore").splitlines():
            k, sep, v = line.strip().partition("=")
            v = v.strip().strip("\"'").removeprefix("api://")
            if not sep or k.startswith("#") or not ID_KEY.search(k) or len(v) < 8 or "..." in v or "<" in v:
                continue
            vals.add(v)
            if GUID.match(v):
                vals.add(v[:8])
    return [v.encode() for v in sorted(vals)]


def allowed(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, g) for g in globs)


def content(spec: str) -> bytes:
    r = subprocess.run(["git", "cat-file", "-p", spec], capture_output=True)
    return r.stdout if r.returncode == 0 else b""


def problems(files: list[tuple[str, str]], globs: list[str], ids: list[bytes] = ()) -> list[str]:
    """files: (path, git object spec for its new content)."""
    out = []
    for path, spec in files:
        why = None
        if not allowed(path, globs):
            why = next((w for pat, w in BLOCKED if re.search(pat, path, re.I)), None)
        if not why:
            data = content(spec)
            why = next((f"contains: {w}" for pat, w in SECRETS if re.search(pat, data)), None)
            if not why and any(re.search(rb"(?<![0-9A-Za-z])" + re.escape(v), data) for v in ids):
                why = "contains: a private id from .env"
        if why:
            out.append(f"  {path}  ({why})")
    return out


def staged() -> list[tuple[str, str]]:
    names = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0")
    return [(n, ":" + n) for n in names if n]


def pushed() -> list[tuple[str, str]]:
    files: dict[str, str] = {}
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) != 4 or parts[1] == ZERO:
            continue
        local, remote = parts[1], parts[3]
        commits = git("rev-list", local, "--not", "--remotes") if remote == ZERO else git("rev-list", f"{remote}..{local}")
        for c in commits.split():
            for n in git("diff-tree", "--no-commit-id", "--name-only", "-r", "--root", "--diff-filter=ACMR", "-z", c).split("\0"):
                if n:
                    files[n] = f"{c}:{n}"
    return list(files.items())


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "commit"
    root = Path(git("rev-parse", "--show-toplevel").strip())
    allow_file = root / ".githooks" / "allow.txt"
    globs = [g.strip() for g in allow_file.read_text(encoding="utf-8").splitlines()
             if g.strip() and not g.startswith("#")] if allow_file.exists() else []
    found = problems(staged() if mode == "commit" else pushed(), globs, private_values(root))
    if not found:
        return 0
    print(f"\nBLOCKED {mode}: these must never go to GitHub.\n" + "\n".join(found), file=sys.stderr)
    print("\nUnstage them (git restore --staged <file>). If one is genuinely safe, such as a diagram we drew,"
          "\nadd its path to .githooks/allow.txt on purpose and commit that change. Ids and secrets are never"
          "\nallowed: write what the value is (\"the agent app's client id, in .env\") instead of the value.\n",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
