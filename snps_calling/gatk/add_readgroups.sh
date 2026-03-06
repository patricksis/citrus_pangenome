#!/usr/bin/env bash
# Add read groups to BAM files using GATK AddOrReplaceReadGroups.
# Usage: bash add_readgroups.sh

# --- Configuration ---
# Directory containing input .bam files
IN_DIR="/path/to/bam_dir"

# Output directory for read-group-tagged .bam files
OUT_DIR="/path/to/rg_bam_dir"

# Sequencing platform (e.g. ILLUMINA, PACBIO)
PLATFORM="ILLUMINA"
# ---------------------

mkdir -p "$OUT_DIR"

for bam in "${IN_DIR}"/*.bam; do
    filename=$(basename "$bam")
    # Adjust this sed pattern to match your sample naming convention
    sample=$(echo "$filename" | sed -E 's/^cut_([A-Za-z0-9]+_[A-Za-z0-9]+_[A-Za-z0-9]+)_.*\.bam$/\1/')

    echo "Adding read groups: $sample"
    gatk AddOrReplaceReadGroups \
        -I "$bam" \
        -O "${OUT_DIR}/${sample}_RG.bam" \
        --RGID "$sample" \
        --RGLB "$sample" \
        --RGPL "$PLATFORM" \
        --RGPU "$sample" \
        --RGSM "$sample"

    samtools index "${OUT_DIR}/${sample}_RG.bam"
done
