#!/usr/bin/env python3
import re
import sys
from collections import Counter


def count_words(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove verse references like [1:1], [10:25], [3:4], etc.
    text = re.sub(r'\[\d+:\d+\]', '', text)

    # Extract words (letters and apostrophes for contractions/possessives)
    words = re.findall(r"[A-Za-z']+", text)

    # Normalize to lowercase for unique word counting
    words_lower = [w.lower().strip("'") for w in words]

    total = len(words_lower)
    unique = len(set(words_lower))

    return total, unique


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 word_count.py <file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]
    total, unique = count_words(filepath)

    print(f"Total words:  {total:,}")
    print(f"Unique words: {unique:,}")


if __name__ == "__main__":
    main()
