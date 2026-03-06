#!/usr/bin/env bash
# Surject GAM alignments to BAM format using vg surject.
# Usage: bash vg_surject.sh

# --- Configuration ---
# Path to the pangenome XG index
XG_INDEX="/path/to/pangenome.xg"

# Directory containing input .gam files
GAM_DIR="/path/to/gam_dir"

# Output directory for .bam files
BAM_DIR="/path/to/bam_dir"

# Number of threads
THREADS=36
# ---------------------

mkdir -p "$BAM_DIR"

for gam_file in "${GAM_DIR}"/*.gam; do
    library_id=$(basename "$gam_file" .gam)
    echo "Surjecting $library_id..."

    vg surject \
        --threads "$THREADS" \
        --xg "$XG_INDEX" \
        --bam \
        --sample "$library_id" \
        --read-group "$library_id" \
        -V \
        "$gam_file" \
        > "${BAM_DIR}/${library_id}.bam"

    echo "Done: ${library_id}.bam"
done
