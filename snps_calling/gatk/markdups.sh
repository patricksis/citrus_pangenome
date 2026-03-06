#!/usr/bin/env bash
# Mark duplicate reads using GATK MarkDuplicates.
# Usage: bash markdups.sh

# --- Configuration ---
# Directory containing input sorted .bam files
IN_DIR="/path/to/sorted_bam_dir"

# Output directory for duplicate-marked .bam files
OUT_DIR="/path/to/markdup_bam_dir"

# Output directory for duplicate metrics
METRICS_DIR="${OUT_DIR}/metrics"
# ---------------------

mkdir -p "$OUT_DIR" "$METRICS_DIR"

for bam in "${IN_DIR}"/*_RG_sorted.bam; do
    sample=$(basename "$bam" _RG_sorted.bam)
    echo "Marking duplicates: $sample"

    gatk MarkDuplicates \
        -I "$bam" \
        -O "${OUT_DIR}/${sample}_markdup.bam" \
        -M "${METRICS_DIR}/${sample}.metrics.txt"

    samtools index "${OUT_DIR}/${sample}_markdup.bam"
done

