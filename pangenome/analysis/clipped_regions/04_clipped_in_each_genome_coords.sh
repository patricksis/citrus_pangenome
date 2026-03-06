#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

ROOT="clipped_regions"
HAP_BEDS="$ROOT/hap_beds"
GENOMES="$ROOT/genomes"
OUT="$ROOT/clipped"
mkdir -p "$OUT"

for b in "$HAP_BEDS"/*.bed; do
  base="$(basename "$b" .bed)"                # e.g. c_reticulata_fortune_primary
  [[ "$base" == "c_reticulata_fortune_primary" ]] && continue  

  hap="${base##*_}"                           # primary|alternate
  stem="${base%_*}"                           # c_australis OR c_reticulata_fallglo

  # map to genomes/<name>.genome
  if [[ "$stem" == c_reticulata_* ]]; then
    var="${stem#c_reticulata_}"
    gfile="$GENOMES/${var}_${hap}.genome"
  else
    sp="${stem#c_}"
    gfile="$GENOMES/C${sp}_${hap}.genome"
  fi

  [[ -s "$gfile" ]] || continue               

  bedtools sort -i "$b" \
    | bedtools merge -i - \
    | bedtools complement -i - -g "$gfile" \
    > "$OUT/${base}.clipped.bed"

  echo "Wrote $OUT/${base}.clipped.bed"
done
