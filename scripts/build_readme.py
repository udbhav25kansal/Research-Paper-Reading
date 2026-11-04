#!/usr/bin/env python3
"""Rebuild the generated parts of README.md from the header of every note in papers/.

    python scripts/build_readme.py           rewrite README.md
    python scripts/build_readme.py --check   exit 1 if README.md is out of date

Each note starts with a header between two --- lines. Required keys: title, field,
date_read, status, one_line. Optional: corrections (a number), threads (a list).
The pre-commit hook runs this on every commit, so the README never goes stale.
Standard library only.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
PAPERS = ROOT / "papers"
REQUIRED = ("title", "field", "date_read", "status", "one_line")
STATUSES = ("Reading", "Verifying", "Done")


def unquote(value: str) -> str:
    value = re.sub(r"\s+#.*$", "", value).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_header(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        sys.exit(f"{path.name}: no header. Copy the top of templates/paper-note.md.")
    meta: dict = {}
    last_key = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and last_key:
            if not isinstance(meta[last_key], list):
                meta[last_key] = []
            meta[last_key].append(unquote(line.lstrip()[2:]))
            continue
        key, _, value = line.partition(":")
        last_key = key.strip()
        meta[last_key] = unquote(value)
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        sys.exit(f"{path.name}: header is missing {', '.join(missing)}.")
    if meta["status"] not in STATUSES:
        sys.exit(f"{path.name}: status must be one of {', '.join(STATUSES)}.")
    meta["link"] = path.relative_to(ROOT).as_posix()
    meta["threads"] = meta.get("threads") or []
    return meta


def cell(text: str) -> str:
    return str(text).replace("|", "\\|")


def build_sections(notes: list[dict]) -> dict[str, str]:
    notes = sorted(notes, key=lambda n: (n["date_read"], n["title"]), reverse=True)
    corrections = sum(int(n.get("corrections") or 0) for n in notes)
    fields = sorted({n["field"] for n in notes})

    stats = "\n".join([
        "| Papers read | Fields | Claims corrected against the source |",
        "|:---:|:---:|:---:|",
        f"| **{len(notes)}** | **{len(fields)}** | **{corrections}** |",
    ])

    if notes:
        n = notes[0]
        latest = f"**[{n['title']}]({n['link']})** ({n['field']}, read {n['date_read']})\n\n> {n['one_line']}"
    else:
        latest = "_No papers yet._"

    log = ["| Read | Paper | Field | The idea in one line | Status |", "|---|---|---|---|---|"]
    for n in notes:
        log.append(f"| {n['date_read']} | [{cell(n['title'])}]({n['link']}) | {cell(n['field'])} "
                   f"| {cell(n['one_line'])} | {n['status']} |")

    by_thread: dict[str, list[dict]] = defaultdict(list)
    for n in notes:
        for t in n["threads"]:
            by_thread[t].append(n)
    threads = []
    for question, papers in sorted(by_thread.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        links = ", ".join(f"[{p['title']}]({p['link']})" for p in papers)
        threads.append(f"- **{question}**  \n  {len(papers)} paper{'s' if len(papers) != 1 else ''}: {links}")
    return {
        "stats": stats,
        "latest": latest,
        "log": "\n".join(log),
        "threads": "\n".join(threads) or "_No threads yet._",
    }


def render(current: str, sections: dict[str, str]) -> str:
    for name, body in sections.items():
        pattern = re.compile(rf"(<!-- BEGIN:{name} -->\n).*?(<!-- END:{name} -->)", re.S)
        if not pattern.search(current):
            sys.exit(f"README.md is missing the {name} markers.")
        current = pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), current)
    return current


def main() -> int:
    notes = [read_header(p) for p in sorted(PAPERS.glob("*.md")) if p.name != "README.md"]
    current = README.read_text(encoding="utf-8")
    updated = render(current, build_sections(notes))
    if "--check" in sys.argv:
        if updated != current:
            print("README.md is out of date. Run: python scripts/build_readme.py")
            return 1
        return 0
    if updated != current:
        README.write_text(updated, encoding="utf-8", newline="\n")
        print("README.md rebuilt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
