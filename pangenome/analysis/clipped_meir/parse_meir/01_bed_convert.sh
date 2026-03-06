wk 'NR>1 {
  snp = $1 ":" $2      # SNP_name = CHROM:POS
  start = $2 - 1       # BED start (0-based)
  end   = $2           # BED end (0-based, half-open)
  print $1, start, end, snp
}' OFS='\t' australis_mier_per_snp_summary.tsv > australis_mier_snps.bed
