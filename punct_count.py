#!/usr/bin/env python3
import os
import re
import sys
from collections import Counter


def extract_punct_patterns(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove verse references like [1:1], [10:25], etc.
    text = re.sub(r'\[\d+:\d+\]', '', text)

    # Split on word tokens (same pattern as word_count.py) — what remains
    # between tokens is purely punctuation and/or whitespace.
    segments = re.split(r"[A-Za-z']+|\d+", text)

    patterns = []
    for seg in segments:
        if not seg:
            continue
        # Normalize any whitespace sequence to a single space so that
        # ", \n" and ",  " and ",\t" all collapse to ", "
        normalized = re.sub(r'\s+', ' ', seg)
        patterns.append(normalized)

    return patterns


def resolve_paths(args):
    paths = []
    for arg in args:
        if os.path.isdir(arg):
            for fname in sorted(os.listdir(arg)):
                if fname.endswith(".txt"):
                    paths.append(os.path.join(arg, fname))
        else:
            paths.append(arg)
    return paths


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 punct_count.py <file.txt> [file2.txt ...] [or directory/]")
        sys.exit(1)

    paths = resolve_paths(sys.argv[1:])

    all_patterns = []
    for path in paths:
        all_patterns.extend(extract_punct_patterns(path))

    total = len(all_patterns)
    counts = Counter(all_patterns)
    unique = len(counts)
    total_chars = sum(len(p) for p in all_patterns)
    unique_chars = sum(len(p) for p in counts)

    print(f"Files:                  {len(paths)}")
    print(f"Total patterns:         {total:,}")
    print(f"Unique patterns:        {unique:,}")
    print(f"Total pattern chars:    {total_chars:,}")
    print(f"Unique pattern chars:   {unique_chars:,}")
    print()
    print("Top 30 patterns (repr shows whitespace):")
    for pattern, count in counts.most_common(30):
        print(f"  {count:>8,}  {repr(pattern)}")


if __name__ == "__main__":
    main()
