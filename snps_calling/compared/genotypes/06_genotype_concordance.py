import pandas as pd

# Load the genotype matrix
df = pd.read_csv("combined_genotype_matrix_normalized.tsv", sep='\t')

# Get all column names except the first ('variant')
genotype_columns = df.columns[1:]

# Extract unique sample names (everything before the last underscore)
sample_names = []
for col in genotype_columns:
    sample = col.rsplit('_', 1)[0]
    if sample not in sample_names:
        sample_names.append(sample)

# Create output DataFrame
concordance_df = pd.DataFrame()
concordance_df["variant"] = df["variant"]

# For each sample, check genotype agreement across callers
for sample in sample_names:
    sample_cols = []
    for col in genotype_columns:
        if col.startswith(sample + "_"):
            sample_cols.append(col)

    concordance_values = []

    for idx, row in df.iterrows():
        genotypes = []
        for col in sample_cols:
            gt = row[col]
            if gt != './.':
                genotypes.append(gt)

        if len(genotypes) == 0:
            concordance_values.append('./.')
        elif len(set(genotypes)) == 1:
            concordance_values.append(1)
        else:
            concordance_values.append(0)

    concordance_df[sample] = concordance_values

# Write to file
concordance_df.to_csv("genotype_concordance_matrix.tsv", sep='\t', index=False)
