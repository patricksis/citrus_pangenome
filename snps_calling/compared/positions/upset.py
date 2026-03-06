import pandas as pd
from upsetplot import UpSet, from_indicators
import matplotlib.pyplot as plt

# Load SNP sets
callers = {
    'vg': 'vg.snps',
    'deepvariant': 'deepvariant.snps',
    'surjected': 'surjected.snps',
    'gatk': 'gatk_linear.snps',
    'bcftools': 'bcftools.snps'
}

snp_sets = {}
for caller, path in callers.items():
    with open(path) as f:
        snp_list = f.read().splitlines()
        snp_sets[caller] = set(snp_list)

# Combine all SNPs
all_snps = set()
for snps in snp_sets.values():
    all_snps.update(snps)
all_snps = sorted(all_snps)

# Build presence/absence matrix
df = pd.DataFrame(index=all_snps)
for caller in callers:
    df[caller] = df.index.isin(snp_sets[caller])

# Convert to UpSet format
data = from_indicators(df.columns, df)

# Plot
plt.figure(figsize=(24, 12))
upset = UpSet(data, show_counts=True, show_percentages=True, sort_by='cardinality', intersection_plot_elements=30)
upset.plot()

# Adjust font sizes
for ax in plt.gcf().axes:
    for label in ax.get_xticklabels():
        label.set_fontsize(9)
        label.set_rotation(90)
    for label in ax.get_yticklabels():
        label.set_fontsize(11)

plt.tight_layout()
plt.savefig("upset_final_readable.png", dpi=300)
