import pandas as pd 
import re 

in_file = "../../MIER_per_snp_summary_surject_bcftools.tsv"
out_file = "surject_bcftools_missing_mier.tsv"

df = pd.read_csv(in_file, sep="\t")

#col_names
meta_cols = [
    "#CHROM", "POS", "total", "missing", "known", "correct",
    "incorrect", "hom_ref", "hom_alt", "het",
    "hom_ref_wrong", "hom_alt_wrong", "het_wrong"
]

sample_cols = [c for c in df.columns if c not in meta_cols]

long = df.melt(id_vars=["#CHROM", "POS"], value_vars=sample_cols, var_name="sample", value_name="code")

incorrect = long[long["code"].isin([5, 9, 17])]

# Rename and save
incorrect = incorrect.rename(columns={"#CHROM": "chrom", "POS": "pos"})
incorrect[["chrom", "pos", "sample"]].to_csv(out_file, sep="\t", index=False)
