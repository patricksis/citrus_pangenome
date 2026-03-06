import pandas as pd

df = pd.read_csv("australis_mier_per_snp_summary.tsv", sep="\t")
df.columns = [c.lstrip("#") for c in df.columns] #removes #

#look at known
df = df[df["known"] > 0].copy()

df["MIER"] = df["incorrect"] / df["known"]

df["SNP_name"] = df["CHROM"].astype(str) + ":" + df["POS"].astype(str)

df[["SNP_name", "MIER", "CHROM", "POS"]].to_csv("australis_snp_mier_tmp.tsv",sep="\t",index=False)
