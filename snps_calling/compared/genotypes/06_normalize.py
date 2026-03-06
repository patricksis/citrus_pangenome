import pandas as pd

df = pd.read_csv("combined_genotype_matrix.tsv", sep="\t")

def normalize_genotype(gt):
    if gt == './.':
        return gt
    gt = gt.replace('|', '/')
    alleles = gt.split('/')
    # Sort alleles to make 0/1 and 1/0 equivalent
    return '/'.join(sorted(alleles))

# Apply 
for col in df.columns[1:]:
    df[col] = df[col].apply(normalize_genotype)
df.to_csv("combined_genotype_matrix_normalized.tsv", sep="\t", index=False)
