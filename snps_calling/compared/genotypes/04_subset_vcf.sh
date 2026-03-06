#!/usr/bin/env bash
# Subset each caller's VCF to shared SNP positions.
# Usage: bash 04_subset_vcf.sh

# --- Configuration ---
FINAL_DIR="/path/to/final_vcf_dir"
POSITIONS="shared_snps.pos"
# ---------------------

bcftools view -R "$POSITIONS" -Ov -o gatk.shared.vcf "${FINAL_DIR}/citrus_surject_combined_SNP_PASS_Q30_BIALLELIC.renamed.vcf.gz"
bcftools view -R "$POSITIONS" -Ov -o vg.shared.vcf "${FINAL_DIR}/vg_merged.final.vcf.gz"
bcftools view -R "$POSITIONS" -Ov -o deepvariant.shared.vcf "${FINAL_DIR}/deepvariant_merged.final.vcf.gz"
bcftools view -R "$POSITIONS" -Ov -o surjected.shared.vcf "${FINAL_DIR}/citrus_surject_combined_SNP_PASS_Q30_BIALLELIC.renamed.vcf.gz"
