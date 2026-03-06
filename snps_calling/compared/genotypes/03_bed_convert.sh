#!/usr/bin/env bash
# Convert shared_snps.txt (CHROM:POS format) to a two-column positions file for bcftools -R.
# Usage: bash 03_bed_convert.sh

awk -F: '{print $1"\t"$2}' shared_snps.txt > shared_snps.pos
