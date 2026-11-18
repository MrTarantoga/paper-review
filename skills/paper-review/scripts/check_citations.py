#!/usr/bin/env python3
"""Check LaTeX citations against BibTeX files.

Usage: check_citations.py main.tex [other.tex ...] [--bib refs.bib ...]

If --bib is not given, bibliography files are discovered from
\\bibliography{...} / \\addbibresource{...} in the .tex files, falling back to
all .bib files next to the first .tex file. Also follows \\input/\\include.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

CITE_RE = re.compile(
    r"\\(?:[a-zA-Z]*cite[a-zA-Z]*\*?|nocite)\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}"
)
BIB_CMD_RE = re.compile(r"\\(?:bibliography|addbibresource)\s*\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)

REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "book": ["title", "publisher", "year"],
    "misc": ["title"],
    "techreport": ["author", "title", "institution", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
}


def strip_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def collect_tex(paths, seen=None):
    seen = seen if seen is not None else set()
    out = []
    for p in paths:
        p = Path(p)
        if not p.exists() and p.with_suffix(".tex").exists():
            p = p.with_suffix(".tex")
        if not p.exists() or p.resolve() in seen:
            continue
        seen.add(p.resolve())
        text = strip_comments(p.read_text(encoding="utf-8", errors="replace"))
        out.append((p, text))
        children = [p.parent / c.strip() for m in INPUT_RE.findall(text) for c in m.split(",")]
        out.extend(collect_tex(children, seen))
    return out


def parse_bib(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    entries = []
    matches = list(ENTRY_RE.finditer(text))
    for i, m in enumerate(matches):
        etype = m.group(1).lower()
        if etype in ("comment", "string", "preamble"):
            continue
        body = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        fields = {f.lower() for f in re.findall(r"(\w+)\s*=", body)}
        line = text.count("\n", 0, m.start()) + 1
        entries.append((m.group(2), etype, fields, line))
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex", nargs="+")
    ap.add_argument("--bib", nargs="*", default=None)
    args = ap.parse_args()

    tex_files = collect_tex(args.tex)
    if not tex_files:
        sys.exit("No readable .tex files found.")

    cites = {}  # key -> list of "file:line"
    bib_paths = []
    for path, text in tex_files:
        for m in CITE_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            for key in m.group(1).split(","):
                key = key.strip()
                if key:
                    cites.setdefault(key, []).append(f"{path}:{line}")
        for m in BIB_CMD_RE.findall(text):
            for b in m.split(","):
                b = b.strip()
                bp = path.parent / (b if b.endswith(".bib") else b + ".bib")
                bib_paths.append(bp)

    if args.bib:
        bib_paths = [Path(b) for b in args.bib]
    if not bib_paths:
        bib_paths = sorted(Path(args.tex[0]).parent.glob("*.bib"))
    bib_paths = [b for b in dict.fromkeys(bib_paths) if b.exists()]
    if not bib_paths:
        sys.exit("No .bib files found (use --bib).")

    entries = []
    for b in bib_paths:
        entries += [(b, *e) for e in parse_bib(b)]
    bib_keys = Counter(e[1] for e in entries)

    print(f"TeX files: {', '.join(str(p) for p, _ in tex_files)}")
    print(f"Bib files: {', '.join(map(str, bib_paths))}")
    print(f"{len(cites)} distinct cited keys, {len(bib_keys)} bib entries\n")

    nocite_all = "*" in cites
    missing = sorted(k for k in cites if k != "*" and k not in bib_keys)
    unused = [] if nocite_all else sorted(k for k in bib_keys if k not in cites)
    dups = sorted(k for k, n in bib_keys.items() if n > 1)

    print("## Cited but missing from bibliography")
    for k in missing:
        print(f"- {k}  (cited at {', '.join(cites[k])})")
    if not missing:
        print("- none")

    print("\n## In bibliography but never cited")
    for k in unused:
        print(f"- {k}")
    if not unused:
        print("- none" + (" (\\nocite{*} used)" if nocite_all else ""))

    print("\n## Duplicate bib keys")
    for k in dups:
        print(f"- {k}")
    if not dups:
        print("- none")

    print("\n## Entries missing common fields")
    any_missing = False
    for b, key, etype, fields, line in entries:
        need = [f for f in REQUIRED.get(etype, []) if f not in fields]
        if "year" in REQUIRED.get(etype, []) and "date" in fields and "year" in need:
            need.remove("year")
        if need:
            any_missing = True
            print(f"- {key} (@{etype}, {b}:{line}): missing {', '.join(need)}")
    if not any_missing:
        print("- none")


if __name__ == "__main__":
    main()
