#!/usr/bin/env python3
import os
import re
import sys


def extract_words(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove verse references like [1:1], [10:25], [3:4], etc.
    text = re.sub(r'\[\d+:\d+\]', '', text)

    # Extract words (letters and apostrophes for contractions/possessives)
    words = re.findall(r"[A-Za-z']+", text)

    # Normalize to lowercase and strip leading/trailing apostrophes
    return [w.lower().strip("'") for w in words]


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
        print("Usage: python3 word_count.py <file.txt> [file2.txt ...] [or directory/]")
        sys.exit(1)

    paths = resolve_paths(sys.argv[1:])

    all_words = []
    for path in paths:
        all_words.extend(extract_words(path))

    total = len(all_words)
    unique = len(set(all_words))

    print(f"Files:        {len(paths)}")
    print(f"Total words:  {total:,}")
    print(f"Unique words: {unique:,}")


if __name__ == "__main__":
    main()
