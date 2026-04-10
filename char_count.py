#!/usr/bin/env python3
import os
import re
import sys
from collections import Counter


def extract_chars(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove verse references like [1:1], [10:25], etc.
    text = re.sub(r'\[\d+:\d+\]', '', text)

    return list(text)


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
        print("Usage: python3 char_count.py <file.txt> [file2.txt ...] [or directory/]")
        sys.exit(1)

    paths = resolve_paths(sys.argv[1:])

    all_chars = []
    for path in paths:
        all_chars.extend(extract_chars(path))

    total = len(all_chars)
    counts = Counter(all_chars)
    unique = len(counts)

    print(f"Files:          {len(paths)}")
    print(f"Total chars:    {total:,}")
    print(f"Unique chars:   {unique}")
    print()
    print("All unique characters (repr, sorted by frequency):")
    for char, count in counts.most_common():
        print(f"  {count:>8,}  {repr(char)}")


if __name__ == "__main__":
    main()
