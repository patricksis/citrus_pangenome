# Install pheatmap if not already installed:
# install.packages("pheatmap")
library(pheatmap)

# Read CSV (first column are row names)
df <- read.csv("citrusheatmap.csv", header = TRUE, row.names = 1, check.names = FALSE)

# Force numeric (handles cases where numbers were read as character)
mat <- as.matrix(df)
mode(mat) <- "numeric"

# Keep only lower triangle (incl diagonal)
mat[upper.tri(mat)] <- NA

# Pretty labels only where not NA
display_mat <- matrix("", nrow(mat), ncol(mat), dimnames = dimnames(mat))
display_mat[!is.na(mat)] <- sprintf("%.2f", mat[!is.na(mat)])

# Fix color scale to a meaningful range (edit if desired)
bk <- seq(50, 100, length.out = 101)

pheatmap(
  mat,
  na_col = "white",
  breaks = bk,
  color = colorRampPalette(c("#d7191c","#fdae61","#ffffbf","#a6d96a","#1a9641"))(100),
  
  cluster_rows = FALSE,
  cluster_cols = FALSE,
  
  display_numbers = display_mat,
  number_color = "black",
  fontsize_number = 14,   # bigger numbers
  
  fontsize_row = 12,
  fontsize_col = 12,
  angle_col = 45,
  
  cellwidth = 55,         
  cellheight = 35,        
  border_color = NA,      # less grid clutter
  
  main = "Caller Genotype Concordance (%)",


  filename = "citrus_heatmap.png",
  width = 12, height = 6
)
