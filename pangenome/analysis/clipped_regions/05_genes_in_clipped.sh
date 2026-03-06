#!/usr/bin/env bash
set -euo pipefail

MAP="clipped/map.tsv"
OUT="clipped/gene_clip_counts.tsv"
echo -e "hap\tgenes_any\tgenes_full\tgenes_partial\ttotal_genes\tpct_any\tpct_full\tpct_partial" > "$OUT"

while read -r base gff; do
  [[ -z "${base:-}" || "$base" =~ ^# ]] && continue

  bed="clipped/${base}.clipped.bed"
  [[ -s "$bed" && -s "$gff" ]] || { echo "skip $base (missing bed or gff)"; continue; }

  genes="$(mktemp)"
  # change 'gene' if needed
  grep -P '\tgene\t' "$gff" > "$genes" || true

  total=$(wc -l < "$genes" | tr -d ' ')
  any=$(bedtools intersect -u -a "$genes" -b "$bed" | wc -l | tr -d ' ')
  full=$(bedtools intersect -u -a "$genes" -b "$bed" -f 1.0 | wc -l | tr -d ' ')
  partial=$(( any - full ))

  if [[ "$total" -gt 0 ]]; then
    pct_any=$(printf "%.4f" "$(echo "100*$any/$total" | bc -l)")
    pct_full=$(printf "%.4f" "$(echo "100*$full/$total" | bc -l)")
    pct_partial=$(printf "%.4f" "$(echo "100*$partial/$total" | bc -l)")
  else
    pct_any="NA"; pct_full="NA"; pct_partial="NA"
  fi

  echo -e "${base}\t${any}\t${full}\t${partial}\t${total}\t${pct_any}\t${pct_full}\t${pct_partial}" >> "$OUT"
  rm -f "$genes"
done < "$MAP"

echo "Wrote $OUT"
