#!/usr/bin/env python3
"""Compare contents of two directories and report differences.

Usage examples:
  ./scripts/compare_adsk_examples.py \
    resources/adsk_python_examples/2025.2.2 \
    resources/adsk_python_examples/2026.2 --detail

Features:
- reports files only in A or only in B
- compares sizes and SHA256 hashes for files present in both
- optional unified diffs for text files when --detail is passed
- skips diffs for large files by default (threshold configurable)
"""

from __future__ import annotations
import argparse
import hashlib
import os
import sys
from pathlib import Path
import difflib

DEFAULT_MAX_DIFF_SIZE = 5 * 1024 * 1024  # 5 MB


def list_files(root: Path):
    files = set()
    for p in root.rglob('*'):
        if p.is_file():
            files.add(p.relative_to(root).as_posix())
    return files


def sha256_of_file(path: Path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def is_text_file(path: Path, blocksize: int = 512) -> bool:
    try:
        with open(path, 'rb') as f:
            chunk = f.read(blocksize)
            if b'\0' in chunk:
                return False
            try:
                chunk.decode('utf-8')
                return True
            except Exception:
                return False
    except Exception:
        return False


def unified_diff(a: Path, b: Path, fromfile: str, tofile: str, max_lines: int | None = None):
    with open(a, 'r', errors='replace') as fa, open(b, 'r', errors='replace') as fb:
        a_lines = fa.readlines()
        b_lines = fb.readlines()
    ud = list(difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile, lineterm=''))
    if max_lines is None:
        return ud
    return ud[:max_lines]


def compare_dirs(dir_a: Path, dir_b: Path, args) -> int:
    a_files = list_files(dir_a)
    b_files = list_files(dir_b)

    only_in_a = sorted(a_files - b_files)
    only_in_b = sorted(b_files - a_files)
    in_both = sorted(a_files & b_files)

    print('\n=== Summary ===')
    print(f'Files only in {dir_a}: {len(only_in_a)}')
    print(f'Files only in {dir_b}: {len(only_in_b)}')
    print(f'Files in both: {len(in_both)}')

    if only_in_a:
        print('\n-- Only in ' + str(dir_a) + ' --')
        for p in only_in_a:
            print(p)

    if only_in_b:
        print('\n-- Only in ' + str(dir_b) + ' --')
        for p in only_in_b:
            print(p)

    diffs_found = 0
    if in_both:
        print('\n-- Differences for files present in both --')
        for rel in in_both:
            a_path = dir_a / rel
            b_path = dir_b / rel
            try:
                a_size = a_path.stat().st_size
                b_size = b_path.stat().st_size
            except FileNotFoundError:
                print(f'[ERROR] Missing during stats: {rel}')
                continue

            if a_size == b_size:
                # quick check: size same, check hash
                a_hash = sha256_of_file(a_path)
                b_hash = sha256_of_file(b_path)
                if a_hash == b_hash:
                    continue
                else:
                    diffs_found += 1
                    print(f'CHANGED: {rel} (same size, different content)')
            else:
                diffs_found += 1
                print(f'CHANGED: {rel} (size {a_size} -> {b_size})')

            if args.detail:
                # Try to show diff if it is a text file and not too large
                if a_size <= args.max_diff_size and b_size <= args.max_diff_size and is_text_file(a_path) and is_text_file(b_path):
                    ud = unified_diff(a_path, b_path, fromfile=str(dir_a / rel), tofile=str(dir_b / rel), max_lines=args.max_diff_lines)
                    if ud:
                        print('\n'.join(ud))
                    else:
                        print('  (no textual diff available)')
                else:
                    print('  (diff skipped: binary or too large)')

    print('\n=== End ===')
    print(f'Differences found: {diffs_found + len(only_in_a) + len(only_in_b)}')
    return 0


def main():
    p = argparse.ArgumentParser(description='Compare contents of two directories')
    p.add_argument('dir_a', nargs='?', default='resources/adsk_python_examples/2025.2.2', help='Left directory (default: %(default)s)')
    p.add_argument('dir_b', nargs='?', default='resources/adsk_python_examples/2026.2', help='Right directory (default: %(default)s)')
    p.add_argument('--detail', action='store_true', help='Show unified diffs for changed text files')
    p.add_argument('--max-diff-size', type=int, default=DEFAULT_MAX_DIFF_SIZE, help='Maximum file size (bytes) to attempt a textual diff (default: 5MB)')
    p.add_argument('--max-diff-lines', type=int, default=200, help='Maximum number of diff lines to show per file (default: 200)')
    args = p.parse_args()

    dir_a = Path(args.dir_a)
    dir_b = Path(args.dir_b)

    if not dir_a.exists() or not dir_a.is_dir():
        print(f'Error: {dir_a} does not exist or is not a directory', file=sys.stderr)
        return 2
    if not dir_b.exists() or not dir_b.is_dir():
        print(f'Error: {dir_b} does not exist or is not a directory', file=sys.stderr)
        return 2

    return compare_dirs(dir_a, dir_b, args)


if __name__ == '__main__':
    raise SystemExit(main())
