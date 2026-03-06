#!/usr/bin/env bash
# Extract SNP positions (CHROM:POS) from each caller's VCF for comparison.
# Loops over all .vcf.gz files in VCF_DIR and outputs a .snps file per caller.
# Usage: bash 01_convert.sh

# --- Configuration ---
# Directory containing per-caller VCF files
VCF_DIR="/path/to/final_vcf_dir"

# Output directory for .snps files
OUT_DIR="."
# ---------------------

mkdir -p "$OUT_DIR"

for vcf in "${VCF_DIR}"/*.vcf.gz; do
    caller=$(basename "$vcf" .vcf.gz)
    echo "Extracting positions: $caller"
    bcftools query -f '%CHROM:%POS\n' "$vcf" | sort -V > "${OUT_DIR}/${caller}.snps"
done
