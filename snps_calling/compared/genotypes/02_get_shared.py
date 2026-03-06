#!/usr/bin/env python3
# Find SNP positions shared across all variant callers.
# Builds a presence/absence matrix and filters for sites called by all callers.
# Output: shared_snps.txt

import pandas as pd

# --- Configuration ---
# Map caller names to their .snps position files (CHROM:POS format)
callers = {
    'vg': 'vg.snps',
    'deepvariant': 'deepvariant.snps',
    'surjected': 'surjected.snps',
    'gatk': 'gatk_linear.snps',
    'bcftools': 'bcftools.snps'
}
# ---------------------

def parse_pos(snp):
    chrom, pos = snp.split(":")
    return (chrom, int(pos))

# Load SNPs from each caller
snp_sets = {}
for name, fname in callers.items():
    with open(fname) as f:
        snp_sets[name] = set(f.read().splitlines())

# Combine and sort all SNP positions
all_snps = set()
for snps in snp_sets.values():
    all_snps.update(snps)
sorted_snps = sorted(all_snps, key=parse_pos)

# Build presence/absence matrix
df = pd.DataFrame(index=sorted_snps)
for name in callers:
    df[name] = df.index.isin(snp_sets[name])

# Filter for SNPs present in all callers
shared = df[df.all(axis=1)].index.tolist()

with open("shared_snps.txt", "w") as out:
    for snp in shared:
        out.write(snp + "\n")
