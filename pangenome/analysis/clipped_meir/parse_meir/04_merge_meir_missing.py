import pandas as pd

# Load MIER table
mier = pd.read_csv("australis_snp_mier_tmp.tsv", sep="\t")[["SNP_name", "MIER"]]

# Load missing haplotypes
missing = pd.read_csv("australis_missing_haps.tsv",sep="\t",header=None,names=["SNP_name", "Inodora_missing_haplotypes"])

# Merge
out = mier.merge(missing, on="SNP_name", how="left")

# Save final table
out.to_csv("australis_SNP_MIER_with_missing_haps.tsv", sep="\t", index=False)
