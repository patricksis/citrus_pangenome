#!/usr/bin/env bash
# Joint genotype DeepVariant gVCFs using GLnexus.
# Usage: bash 02_glnexus.sh

# --- Configuration ---
# GLnexus Singularity image
SIF="/path/to/glnexus.sif"

# Directory containing per-sample .g.vcf.gz files
GVCF_DIR="/path/to/gvcf_dir"

# Output file prefix
OUT_PREFIX="deepvariant_merged"

# Threads for bgzip compression
BGZIP_THREADS=4
# ---------------------

# Run GLnexus joint genotyping
singularity exec "$SIF" \
  glnexus_cli --config DeepVariant "${GVCF_DIR}"/*.g.vcf.gz > "${OUT_PREFIX}.bcf"

# Convert to bgzipped VCF and index
bcftools view "${OUT_PREFIX}.bcf" | bgzip -@ "$BGZIP_THREADS" -c > "${OUT_PREFIX}.vcf.gz"
tabix -p vcf "${OUT_PREFIX}.vcf.gz"

# Remove intermediate BCF
rm "${OUT_PREFIX}.bcf"
