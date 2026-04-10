#!/usr/bin/env python3
import os
import re
import sys
from collections import Counter


def extract_tokens(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove verse references like [1:1], [10:25], etc.
    text = re.sub(r'\[\d+:\d+\]', '', text)

    # Split while keeping word tokens — produces [sep, word, sep, word, ...]
    parts = re.split(r"([A-Za-z']+|\d+)", text)

    tokens = []
    # Word tokens sit at odd indices; trailing separator follows at index+1
    for i in range(1, len(parts), 2):
        word = parts[i].lower().strip("'")
        trailing = parts[i + 1] if i + 1 < len(parts) else ''
        # Normalize any whitespace sequence to a single space
        trailing = re.sub(r'\s+', ' ', trailing)
        tokens.append(word + trailing)

    return tokens


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
        print("Usage: python3 token_count.py <file.txt> [file2.txt ...] [or directory/]")
        sys.exit(1)

    paths = resolve_paths(sys.argv[1:])

    all_tokens = []
    for path in paths:
        all_tokens.extend(extract_tokens(path))

    total = len(all_tokens)
    counts = Counter(all_tokens)
    unique = len(counts)

    print(f"Files:         {len(paths)}")
    print(f"Total tokens:  {total:,}")
    print(f"Unique tokens: {unique:,}")
    print()
    print("Top 30 tokens (repr shows whitespace):")
    for token, count in counts.most_common(30):
        print(f"  {count:>8,}  {repr(token)}")


if __name__ == "__main__":
    main()
