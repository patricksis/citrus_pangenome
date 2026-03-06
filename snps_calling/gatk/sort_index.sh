#!/usr/bin/env bash
# Sort and index BAM files using samtools.
# Usage: bash sort_index.sh

# --- Configuration ---
# Directory containing input read-group-tagged .bam files
BAM_DIR="/path/to/rg_bam_dir"

# Output directory for sorted .bam files
SORTED_DIR="/path/to/sorted_bam_dir"
# ---------------------

mkdir -p "$SORTED_DIR"

for bam in "${BAM_DIR}"/*_RG.bam; do
    sample=$(basename "$bam" _RG.bam)

    echo "Sorting: $sample"
    samtools sort -o "${SORTED_DIR}/${sample}_RG_sorted.bam" "$bam"

    echo "Indexing: $sample"
    samtools index "${SORTED_DIR}/${sample}_RG_sorted.bam"
done
