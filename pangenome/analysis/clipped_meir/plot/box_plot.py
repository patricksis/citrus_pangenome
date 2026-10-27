import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# input files (keys control x-axis labels AND pval lookup)
files = {
    "C. australis":    "australis_SNP_MIER_with_missing_haps.tsv",
    "C. australasica": "australasica_SNP_MIER_with_missing_haps.tsv",
    "C. inodora":      "SNP_MIER_with_missing_haps.tsv",
}

species_names = list(files.keys())
missing_levels = [0, 1, 2]

groups = []

# extract hap groups
for species in species_names:
    df = pd.read_csv(files[species], sep="\t")
    df["Inodora_missing_haplotypes"] = df["Inodora_missing_haplotypes"].astype(int)
    for missing in missing_levels:
        groups.append(df.loc[df["Inodora_missing_haplotypes"] == missing, "MIER"].dropna())

# plot
n_species = len(species_names)
positions = list(range(1, n_species * 3 + 1))

plt.figure(figsize=(14, 6))
ax = plt.gca()

ax.boxplot(groups, positions=positions, showfliers=False)

# add mean ± SD lines
for pos, g in zip(positions, groups):
    g = g.dropna()
    if len(g) < 2:
        continue
    mean = np.mean(g)
    std = np.std(g, ddof=1)
    ax.hlines(
        [mean - std, mean + std],
        pos - 0.2,
        pos + 0.2,
        colors="gray",
        linestyles="dashed",
        linewidth=1,
    )

tick_labels = [str(m) for _ in range(n_species) for m in missing_levels]
ax.set_xticks(positions)
ax.set_xticklabels(tick_labels, fontsize=11)

ax.set_ylabel("MIER")
ax.set_xlabel("Missing haplotypes", labelpad=25)
ax.set_title("MIER vs Missing Haplotypes", fontsize=16)

# lines between species
for i in range(1, n_species):
    ax.axvline(i * 3 + 0.5, color="black", linestyle="--", linewidth=1, alpha=0.6)

# species labels under groups
species_centers = [i * 3 + 2 for i in range(n_species)]
for x, name in zip(species_centers, species_names):
    ax.text(
        x,
        -0.08,
        name,
        ha="center",
        va="top",
        fontsize=12,
        transform=ax.get_xaxis_transform(),
    )

# p values (keys MUST match species_names exactly)
pvals = {
    "C. australis": {
        (0, 1): 1.249342e-07,
        (0, 2): 4.359657e-18,
        (1, 2): 6.926180e-02,
    },
    "C. australasica": {
        (0, 1): 1.812251e-11,
        (0, 2): 2.933287e-26,
        (1, 2): 2.316381e-02,
    },
    "C. inodora": {
        (0, 1): 0.789528,
        (0, 2): 5.0e-06,
        (1, 2): 6.09e-04,
    },
}

def format_p(p):
    if p < 1e-3:
        return f"p={p:.2e}"
    else:
        return f"p={p:.3f}"

def add_bracket(ax, x1, x2, y, h, text, fs=9):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.2, c="black")
    ax.text((x1 + x2) / 2, y + h, text, ha="center", va="bottom", fontsize=fs)

# y-limits and bracket layout
y_max = max(float(g.max()) for g in groups if len(g) > 0)
ax.set_ylim(0, y_max * 1.40)

base_y = y_max * 1.05
step_y = y_max * 0.08
h = y_max * 0.015

pair_to_level = {(0, 1): 0, (1, 2): 1, (0, 2): 2}

for s_idx, species in enumerate(species_names):
    base = s_idx * 3 + 1
    x_pos = {0: base + 0, 1: base + 1, 2: base + 2}

    for pair, level in pair_to_level.items():
        p = pvals.get(species, {}).get(pair)
        if p is None:
            continue
        label = format_p(p)
        x1, x2 = x_pos[pair[0]], x_pos[pair[1]]
        y = base_y + level * step_y
        add_bracket(ax, x1, x2, y, h, label, fs=9)

plt.tight_layout()
plt.savefig("limes_mier_by_missing_haps_boxplot_with_pvalue_brackets.png", dpi=300)
plt.close()
