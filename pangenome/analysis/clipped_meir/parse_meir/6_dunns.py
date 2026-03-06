mport pandas as pd
import scikit_posthocs as sp

df = pd.read_csv("australis_SNP_MIER_with_missing_haps.tsv", sep="\t")
df["Inodora_missing_haplotypes"] = df["Inodora_missing_haplotypes"].astype(int)

# downsample 10k SNPs
df_sub = df.sample(10000, random_state=0)

dunn_sub = sp.posthoc_dunn(
    df_sub,
    val_col="MIER",
    group_col="Inodora_missing_haplotypes",
)
    #p_adjust="fdr_bh"


print(dunn_sub)
