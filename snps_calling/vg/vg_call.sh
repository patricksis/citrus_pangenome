#!/usr/bin/env bash
# Call variants from vg pack files against a pangenome graph.
# Usage: bash vg_call.sh

# --- Configuration ---
# Path to the pangenome XG index
XG_INDEX="/path/to/pangenome.xg"

# Directory containing input .pack files
PACK_DIR="/path/to/pack_dir"

# Output directory for .vcf files
OUTPUT_DIR="/path/to/output_dir"
# ---------------------

mkdir -p "$OUTPUT_DIR"

for pack in "${PACK_DIR}"/*.pack; do
    sample_name=$(basename "$pack" .pack)
    echo "Calling variants for sample: $sample_name"
    vg call "$XG_INDEX" -k "$pack" > "${OUTPUT_DIR}/${sample_name}.vcf"
done
