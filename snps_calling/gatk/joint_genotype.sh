#!/usr/bin/env bash
# Run GATK HaplotypeCaller in GVCF mode on each sample.
# Usage: bash joint_genotype.sh

# --- Configuration ---
# Reference genome (must be indexed with samtools faidx and gatk CreateSequenceDictionary)
REF="/path/to/reference.fasta"

# Directory containing duplicate-marked .bam files
IN_DIR="/path/to/markdup_bam_dir"

# Output directory for per-sample .g.vcf.gz files
OUT_DIR="/path/to/gvcf_dir"

# Java memory settings
JAVA_MEM="-Xms32G -Xmx32G -XX:ParallelGCThreads=2"

# HMM threads
HMM_THREADS=8
# ---------------------

mkdir -p "$OUT_DIR"

for bam in "${IN_DIR}"/*_markdup.bam; do
    sample=$(basename "$bam" _markdup.bam)
    echo "Running HaplotypeCaller: $sample"

    gatk HaplotypeCaller \
        --java-options "$JAVA_MEM" \
        -R "$REF" \
        -I "$bam" \
        -O "${OUT_DIR}/${sample}.g.vcf.gz" \
        -ERC GVCF \
        --native-pair-hmm-threads "$HMM_THREADS"
done
