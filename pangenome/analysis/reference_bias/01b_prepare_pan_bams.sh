mkdir -p ../1_prepare/pan

for f in ../input/pangenome_bams/bams_fixed/*.bam; do
  # Extract sample name from everything between 'cut_' and the first '.' before '.bam'
  id=$(basename "$f" | sed -E 's/^cut_([A-Za-z0-9]+_[0-9]+_[0-9]+).*\.bam/\1/')
  out="../1_prepare/pan/${id}_pan_filtered.bam"
  bash 1-prepare-bam.sh "$f" "$out" 24
done
