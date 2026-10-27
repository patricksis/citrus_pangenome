#!/usr/bin/env bash
# Build the citrus super-pangenome with Minigraph-Cactus.
# Usage: bash 01_construction.sh

# --- Configuration ---
BIND_DIR="/path/to/analysis_dir"
CACTUS_IMAGE="/path/to/cactus_v2.9.3.sif"
REFERENCE="c_reticulata_fortune_primary"
# ---------------------

# Reduced (clipped) graph, used for short-read mapping
singularity exec -B "$BIND_DIR" "$CACTUS_IMAGE" \
    cactus-pangenome ./js ./citrus_mc.seqfile.txt \
    --outDir ./citrus-pg --outName citrus-pg \
    --reference "$REFERENCE" --vcf --giraffe --gfa --gbz

# Full (unclipped) graph
singularity exec -B "$BIND_DIR" "$CACTUS_IMAGE" \
    cactus-pangenome ./js ./citrus_mc_haps.seqfile.txt \
    --outDir ./citrus-pg-full --outName citrus-pg-full \
    --reference "$REFERENCE" --vcf --gfa full --viz
