library(UpSetR)
library(tidyverse)

# Load
pav_file <- "merged_pav_matrix_with_duplicates.tsv"
pav_df <- read.delim(pav_file, header=TRUE, sep="\t", stringsAsFactors=FALSE)

# Make duplicate gene IDs unique
pav_df$gene_id <- make.unique(pav_df$gene_id)

pav_df <- pav_df %>%
  column_to_rownames(var="gene_id")

#UpSet plot
upset(pav_df, 
      sets=colnames(pav_df), 
      order.by="freq", 
      mainbar.y.label="Number of Genes",
      sets.x.label="Genomes",
      keep.order=TRUE,
      text.scale = c(1.5, 1.5, 1.5, 1.2, 1.2, 1.2)  # Adjust text size
)
