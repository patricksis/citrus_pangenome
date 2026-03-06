#!/usr/bin/env bash
# Compute read support (pack) from GAM alignments for variant calling.
# Usage: bash vg_pack.sh

# --- Configuration ---
# Path to the pangenome XG index
XG_INDEX="/path/to/pangenome.xg"

# Directory containing input .gam files
GAM_DIR="/path/to/gam_dir"

# Output directory for .pack files
OUTPUT_DIR="/path/to/output_dir"

# Minimum mapping quality to include a read
MIN_MAPQ=5
# ---------------------

mkdir -p "$OUTPUT_DIR"

for gam in "${GAM_DIR}"/*.gam; do
    sample_name=$(basename "$gam" .gam)
    echo "Packing sample: $sample_name"
    vg pack -x "$XG_INDEX" -g "$gam" -Q "$MIN_MAPQ" -o "${OUTPUT_DIR}/${sample_name}.pack"
done
