import pandas as pd

pav_file = "findplantnlr_pav_matrix.tsv"
pav_df = pd.read_csv(pav_file, sep="\t")

gene_presence = pav_df.iloc[:, 1:]

num_genomes = gene_presence.shape[1]

core_genes = gene_presence.sum(axis=1) == num_genomes

private_genes = gene_presence.sum(axis=1) == 1

accessory_genes = (gene_presence.sum(axis=1) > 1) & (gene_presence.sum(axis=1) < num_genomes)

gene_counts = {
    "Core Genes": core_genes.sum(),
    "Accessory Genes": accessory_genes.sum(),
    "Private Genes": private_genes.sum(),
}

with open("NLR_gene_category_counts.txt", "w") as f:
    for category, count in gene_counts.items():
        f.write(f"{category}: {count}\n")
