bedtools intersect -c \
  -a australis_mier_snps.bed \
  -b ../files/australis1.clipped.merged.bed \
  > australis_snps_primary.bed

bedtools intersect -c \
  -a australis_mier_snps.bed \
  -b ../files/australis2.clipped.merged.bed \
  > australis_snps_alternate.bed
