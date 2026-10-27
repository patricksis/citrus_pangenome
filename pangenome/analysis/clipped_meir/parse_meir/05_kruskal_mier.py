import pandas as pd
from scipy.stats import kruskal
from scipy import stats

# Load data
df = pd.read_csv("australis_SNP_MIER_with_missing_haps.tsv", sep="\t")
df["Inodora_missing_haplotypes"] = df["Inodora_missing_haplotypes"].astype(int)

# Extract groups
g0 = df[df["Inodora_missing_haplotypes"] == 0]["MIER"]
g1 = df[df["Inodora_missing_haplotypes"] == 1]["MIER"]
g2 = df[df["Inodora_missing_haplotypes"] == 2]["MIER"]

# Kruskal–Wallis test
stat, p = kruskal(g0, g1, g2)

result = stats.kruskal(g0, g1, g2)
print(result)
