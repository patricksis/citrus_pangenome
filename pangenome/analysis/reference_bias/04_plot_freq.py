import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("alt_freq_stats.tsv", sep="\t")

# Sort samples
library_order = sorted(df["library"].unique())

# plot
g = sns.catplot(
    data=df,
    x="library",
    y="mean",
    hue="aligner",
    kind="strip",
    order=library_order,
    aspect=5,
    height=3
)

g.set(ylim=(0.4, 0.5), xlabel="Sample", ylabel="Mean Alt Fraction")
plt.axhline(0.5, color="grey", linestyle="--")
plt.xticks(rotation=90)

g._legend.set_bbox_to_anchor((1.05, 0.5))
g._legend.set_frame_on(False)

plt.tight_layout()
plt.savefig("alt_allele_freq_f1s.png", dpi=300, bbox_inches="tight")
