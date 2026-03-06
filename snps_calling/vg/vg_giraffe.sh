#!/usr/bin/env bash
# Map short reads to a pangenome graph using vg giraffe.
# Usage: bash vg_giraffe.sh

# --- Configuration ---
# Directory containing the vg index files (.gbz, .min, .zipcodes, .dist)
INDEX_DIR="/path/to/index_dir"

# File listing R1 fastq paths (one per line); R2 inferred by replacing _1.fq.gz with _2.fq.gz
FASTQ_LIST="/path/to/fastq_list.txt"

# Output directory for .gam alignment files
OUTPUT_DIR="/path/to/output_dir"

# Prefix of the vg index files
INDEX_PREFIX="pangenome"

# Number of threads
THREADS=12
# ---------------------

mkdir -p "$OUTPUT_DIR"

while read -r R1; do
    R2="${R1%%_1.fq.gz}_2.fq.gz"
    base=$(basename "$R1" _1.fq.gz)
    echo "Processing sample: $base"

    vg giraffe \
        -Z "${INDEX_DIR}/${INDEX_PREFIX}.giraffe.gbz" \
        -m "${INDEX_DIR}/${INDEX_PREFIX}.shortread.withzip.min" \
        -z "${INDEX_DIR}/${INDEX_PREFIX}.shortread.zipcodes" \
        -d "${INDEX_DIR}/${INDEX_PREFIX}.dist" \
        -t "$THREADS" \
        -f "$R1" \
        -f "$R2" \
        > "${OUTPUT_DIR}/${base}.gam" 2> "${OUTPUT_DIR}/${base}.log"

done < "$FASTQ_LIST"
