# Citrus Pangenome SNP Benchmarking

Preprint: Kuster R, Sisler P, et al. (2026). *Benchmarking SNP-Calling Accuracy Against Known Citrus Pedigrees Reveals Pangenome Advantages Over Linear References.* bioRxiv. https://www.biorxiv.org/content/10.64898/2026.04.07.716967v1

A benchmarking study comparing SNP variant calling approaches using a citrus pangenome graph. Six calling strategies are evaluated across shared variant sites, with genotype concordance analysis between callers.

## Overview

Short reads are mapped either to a minigraph-cactus pangenome graph using `vg giraffe` or to a linear reference using BWA-MEM. SNPs are then called via six strategies:

| Strategy | Mapping | Caller |
|----------|---------|--------|
| vg (pangenome-native) | vg giraffe | vg pack + vg call |
| vg-surject → GATK | vg giraffe → surject to BAM | GATK HaplotypeCaller |
| vg-surject → bcftools | vg giraffe → surject to BAM | bcftools (via Nextflow) |
| Linear GATK | BWA-MEM | GATK HaplotypeCaller |
| Linear bcftools | BWA-MEM | bcftools |
| DeepVariant | BWA-MEM | DeepVariant + GLnexus |

Calls are then compared at the position and genotype level to benchmark pangenome-based calling against linear reference approaches.

## Dependencies

- [vg](https://github.com/vgteam/vg)
- [samtools](http://www.htslib.org/)
- [GATK](https://gatk.broadinstitute.org/)
- [bcftools](https://samtools.github.io/bcftools/)
- [DeepVariant](https://github.com/google/deepvariant) (via Singularity)
- [GLnexus](https://github.com/dnanexus-rnd/GLnexus) (via Singularity)
- [Nextflow](https://www.nextflow.io/) + `vary_cool` pipeline (for bcftools/linear GATK calling)
- Python: `pandas`, `upsetplot`, `matplotlib`
- R: `pheatmap`

## Pipeline Steps

Edit the `# --- Configuration ---` block at the top of each script before running.

### Pangenome Mapping

```bash
bash snps_calling/vg/vg_giraffe.sh    # Map reads to pangenome graph
bash snps_calling/vg/vg_surject.sh    # Surject GAM alignments to BAM
```

### SNP Calling

```bash
# Pangenome-native
bash snps_calling/vg/vg_pack.sh       # Compute read support
bash snps_calling/vg/vg_call.sh       # Call variants from graph

# Surjected reads → linear callers
bash snps_calling/gatk/add_readgroups.sh
bash snps_calling/gatk/sort_index.sh
bash snps_calling/gatk/markdups.sh
bash snps_calling/gatk/joint_genotype.sh   # GATK HaplotypeCaller (GVCF mode)

# DeepVariant (SLURM array job)
sbatch --array=0-N snps_calling/deepvariant/01_run_deepvariant.qsh
bash snps_calling/deepvariant/02_glnexus.sh   # Joint genotyping with GLnexus

# bcftools and linear GATK are run via the vary_cool Nextflow pipeline
# See: snps_calling/bcftools/run_bcftools.qsh and snps_calling/gatk/run_haplotype_caller.qsh
```

### Benchmarking

#### Position-level comparison
```bash
bash snps_calling/compared/positions/01_convert.sh   # Extract CHROM:POS from each VCF
python3 snps_calling/compared/positions/upset.py      # UpSet plot of shared/unique positions
```

#### Genotype-level comparison
```bash
bash snps_calling/compared/genotypes/convert.sh          # Extract positions per caller
python3 snps_calling/compared/genotypes/02_get_shared.py # Find sites shared across all callers
bash snps_calling/compared/genotypes/03_bed_convert.sh   # Convert to positions file
bash snps_calling/compared/genotypes/04_subset_vcf.sh    # Subset each VCF to shared sites
python3 snps_calling/compared/genotypes/05_make_matrix.py       # Build genotype matrix
python3 snps_calling/compared/genotypes/06_normalize.py          # Normalize genotype encoding
python3 snps_calling/compared/genotypes/06_genotype_concordance.py  # Compute concordance
Rscript snps_calling/compared/genotypes/07_heatmap.R             # Concordance heatmap
```

## Pangenome Analysis

Additional analyses on the pangenome graph:

- `pangenome/analysis/gene_pav/` — Gene presence/absence variation
- `pangenome/analysis/clipped_regions/` — Regions clipped during graph construction
- `pangenome/analysis/reference_bias/` — Reference allele bias comparison between linear and pangenome mapping
- `pangenome/analysis/clipped_meir/` — Statistical analysis of clipped region variants

## Input Files

| File | Description |
|------|-------------|
| `*.fq.gz` | Paired-end short reads (one R1/R2 pair per sample) |
| `pangenome.giraffe.gbz` | vg giraffe index |
| `pangenome.xg` | vg XG index |
| `reference.fasta` | Linear reference genome |

## Key Output Files

- `*.gam` — Graph alignments (vg giraffe)
- `*.vcf` / `*.vcf.gz` — Per-caller variant calls
- `shared_snps.txt` — SNP positions called by all callers
- `combined_genotype_matrix_normalized.tsv` — Normalized genotype matrix
- `genotype_concordance_matrix.tsv` — Per-sample concordance across callers
- `upset_final_readable.png` — UpSet plot of position overlap
- `citrus_heatmap.png` — Genotype concordance heatmap
