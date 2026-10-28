#!/usr/bin/env bash
# Download and extract the dataset shards from the GitHub release.
#
#   scripts/download.sh                 # all shards into ./data
#   scripts/download.sh data core-legal charts
#
# Shard names: core-<industry> (9 shards), charts, styles.
set -euo pipefail

REPO="cloudraker/cloudraker-synthdocs"
TAG="${SYNTHDOCS_TAG:-v1.0}"
OUT="${1:-data}"
shift || true
mkdir -p "$OUT"
cd "$OUT"

if [ "$#" -eq 0 ]; then
  patterns=("synthdocs-*.tar")
else
  patterns=()
  for s in "$@"; do patterns+=("synthdocs-$s.tar"); done
fi

args=()
for p in "${patterns[@]}"; do args+=(--pattern "$p"); done
gh release download "$TAG" --repo "$REPO" --clobber "${args[@]}" --pattern SHA256SUMS

grep -F -f <(ls synthdocs-*.tar) SHA256SUMS | shasum -a 256 -c -
for t in synthdocs-*.tar; do
  tar -xf "$t" && rm "$t"
done
echo "Done: $(find . -name '*.json' | wc -l | tr -d ' ') pages in $OUT"
