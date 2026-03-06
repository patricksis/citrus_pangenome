#!/usr/bin/env python3
# Merge per-caller genotype TSVs into a combined genotype matrix.
# Output: combined_genotype_matrix.tsv

import pandas as pd
from functools import reduce

# Manually provided sample names (36 total)
sample_names = [
    "F1_1682_01", "F1_1689_01", "F1_1689_02", "F1_1729_02", "F1_1735_01", "F1_1755_02",
    "F1_191_03", "F1_196_01", "F1_199_01", "F1_242_01", "F1_246_01", "F1_247_01",
    "F1_254_01", "F1_334_01", "F1_359_01", "F1_41_02", "F1_41_03", "F1_411_02",
    "F1_449_01", "F1_449_03", "F1_459_01", "F1_459_02", "F1_471_01", "F1_471_02",
    "F1_475_01", "F1_475_02", "F1682_02_96", "F1731_02_87", "F199_02_90", "F313_01_95",
    "Pr_For_79", "Pr_Ino_85", "Prnt_Fallglo", "Prnt_MAsica", "Prnt_MAuslis", "Prnt_Wilking"
]

# Define input genotype files for each caller
caller_files = {
    "gatk": "gatk.genotypes.tsv",
    "vg": "vg.genotypes.dedup.tsv",
    "bcftools": "bcftools.genotypes.tsv",
    "gatk-surject": "surjected.genotypes.tsv",
    "deepvariant": "deepvariant.genotypes.tsv"
}

# List to hold all DataFrames
dataframes = []

# Process each file
for caller in caller_files:
    filepath = caller_files[caller]

    # Read file, no header
    df = pd.read_csv(filepath, sep='\t', header=None)

    # Rename the first column to 'variant'
    df.rename(columns={0: "variant"}, inplace=True)

    # Rename genotype columns using real sample names and the caller
    for i in range(1, len(df.columns)):
        column_index = i
        sample = sample_names[i - 1]
        new_column_name = f"{sample}_{caller}"
        df.rename(columns={column_index: new_column_name}, inplace=True)

    dataframes.append(df)

# Merge all DataFrames on the 'variant' column
merged_df = dataframes[0]
for i in range(1, len(dataframes)):
    merged_df = pd.merge(merged_df, dataframes[i], on="variant")

# Save final merged genotype matrix
merged_df.to_csv("combined_genotype_matrix.tsv", sep='\t', index=False)
