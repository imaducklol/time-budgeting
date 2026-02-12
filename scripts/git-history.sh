#!/usr/bin/env bash
set -euo pipefail

# Get all Git-tracked files
files=$(git ls-files)

for f in $files; do
    created=$(git log --follow --diff-filter=A -1 --format="%aI" -- "$f")
    updated=$(git log --follow -1 --format="%aI" -- "$f")

    echo "---------- $f ----------"
    echo "created: $created"
    echo "updated: $updated"
    echo
done