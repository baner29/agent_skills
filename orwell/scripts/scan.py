#!/usr/bin/env python3
"""Mechanical scan for the Orwell skill.

Applies references/banned-ai-words.md to a text file and reports hits,
sentence statistics, and em dash count. It counts; it does not judge.
Hits inside quotation marks may be examples held up for scorn, not
faults. That call belongs to the reader.

Usage: python3 scan.py <text-file> [--list <banned-list-file>]
Default list: ../references/banned-ai-words.md relative to this script.
Standard library only.
"""

import argparse
import re
import sys
from pathlib import Path


FUNCTION_WORDS = {
    "is", "has", "to", "a", "an", "the", "of", "in", "on", "be", "are",
    "was", "were", "it", "as", "at", "by", "for", "or", "and", "have",
}


def normalize(s: str) -> str:
    return (
        s.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .lower()
    )


def parse_list(text: str):
    """Return (words, phrases) extracted from the banned-list markdown."""
    words, phrases = set(), set()
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line
            continue
        if section is None:
            continue
        if section.startswith("## 1."):
            m = re.match(r"- \*\*[^*]+:\*\*\s*(.+)", line)
            if m:
                for item in m.group(1).split(","):
                    item = re.sub(r"\([^)]*\)", "", item).strip().rstrip(".")
                    if item:
                        words.add(normalize(item))
        elif section.startswith(("## 2.", "## 3.")):
            for q in re.findall(r'"([^"]+)"', line):
                # Templates like "In today's [fast-paced / digital] world":
                # keep the first bracketed alternative as a concrete phrase.
                q = re.sub(r"\[([^\]]+)\]",
                           lambda m: m.group(1).split("/")[0].strip(), q)
                q = q.split(" / ")[0].strip().strip(".").rstrip(".")
                q = q.lstrip(".")
                if not q:
                    continue
                if " " not in q and normalize(q) in FUNCTION_WORDS:
                    continue  # quoted asides like (use "to"), (prefer "is")
                if re.search(r"(?<![\w'])X(?![\w'])|(?<![\w'])Y(?![\w'])", q):
                    continue  # placeholder pattern like "Not X, but Y"
                nq = normalize(q)
                if " " in nq:
                    phrases.add(nq)
                else:
                    words.add(nq)
        elif section.startswith("## 4."):
            m = re.match(r"- (.+)", line)
            if m and "Empty by default" not in line:
                term = re.split(r"\s+[\u2014\u2013]\s+", m.group(1))[0]
                term = term.strip().strip("*`").rstrip(".")
                if term and len(term.split()) <= 6:
                    nq = normalize(term)
                    (phrases if " " in nq else words).add(nq)
    return sorted(words), sorted(phrases)


def main() -> int:
    ap = argparse.ArgumentParser(description="Orwell mechanical scan")
    ap.add_argument("file", help="text file to scan")
    ap.add_argument("--list", dest="listfile", default=None,
                    help="banned list markdown (default: skill's own list)")
    args = ap.parse_args()

    list_path = Path(args.listfile) if args.listfile else (
        Path(__file__).resolve().parent.parent / "references" / "banned-ai-words.md"
    )
    if not list_path.exists():
        print(f"banned list not found: {list_path}", file=sys.stderr)
        return 1
    target = Path(args.file)
    if not target.exists():
        print(f"text file not found: {target}", file=sys.stderr)
        return 1

    words, phrases = parse_list(list_path.read_text(encoding="utf-8"))
    raw = target.read_text(encoding="utf-8")
    lines = raw.splitlines()
    norm_lines = [normalize(l) for l in lines]

    hits = []  # (line_no, term, count)
    for i, nl in enumerate(norm_lines, 1):
        for w in words:
            n = len(re.findall(r"\b" + re.escape(w) + r"\w*", nl))
            if n:
                hits.append((i, w, n))
        for p in phrases:
            n = nl.count(p)
            if n:
                hits.append((i, p, n))
    hits.sort()

    print(f"Scanned {target} against {list_path.name}: "
          f"{len(words)} words, {len(phrases)} phrases on the list.")
    if hits:
        print(f"\nBanned-list hits: {sum(c for _, _, c in hits)}")
        for ln, term, n in hits:
            excerpt = lines[ln - 1].strip()
            if len(excerpt) > 100:
                excerpt = excerpt[:97] + "..."
            print(f'  line {ln}: "{term}" x{n} - {excerpt}')
    else:
        print("\nBanned-list hits: 0")

    flat = normalize(raw)
    sentences = [s for s in re.finditer(r"[^.!?]+[.!?]+", flat)]
    lengths = [len(s.group(0).split()) for s in sentences]
    if lengths:
        long_s = [(raw[: s.start()].count("\n") + 1, L, s.group(0).strip())
                  for s, L in zip(sentences, lengths) if L > 30]
        print(f"\nSentences: {len(lengths)} | average "
              f"{sum(lengths) / len(lengths):.1f} words | {len(long_s)} over 30 words")
        for ln, L, s in long_s:
            print(f'  long: line {ln} ({L} words): "{s[:70]}..."')
    print(f"Em dashes: {raw.count(chr(0x2014))}")
    print("\nNote: hits inside quotation marks may be examples, not faults. "
          "Judgment belongs to the reader.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
