paste australis_snps_primary.bed australis_snps_alternate.bed \
| awk 'BEGIN{OFS="\t"} {
    snp = $4               # SNP name
    h1  = $5               # hap1 missing (0 or 1)
    h2  = $10              # hap2 missing (0 or 1)
    missing = (h1 > 0) + (h2 > 0)
    print snp, missing
}' > australis_missing_haps.tsv
