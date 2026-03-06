mkdir -p ../1_prepare/{linear,pan}

for f in ../input/linear_bams/*.bam; do
  # Extract sample name: get everything between 'cut_' and the last underscore before '.bam'
  id=$(basename "$f" | sed -E 's/^cut_([^_]+_[^_]+_[^_]+).*\.bam/\1/')
  out="../1_prepare/linear/${id}_linear_filtered.bam"
  bash 1-prepare-bam.sh "$f" "$out" 24
done
