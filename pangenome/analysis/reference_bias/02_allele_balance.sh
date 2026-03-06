kdir -p ../2_calc-allele-balance/{linear,pan}

# Linear
for f in ../1_prepare/linear/*.bam; do
  id=$(basename "$f" | sed -E 's/_linear_filtered\.bam//')
  out="../2_calc-allele-balance/linear/${id}_linear.tsv"
  bash 2-calc-allele-balance.sh "$f" "$out"
done

# Pan
for f in ../1_prepare/pan/*.bam; do
  id=$(basename "$f" | sed -E 's/_pan_filtered\.bam//')
  out="../2_calc-allele-balance/pan/${id}_pan.tsv"
  bash 2-calc-allele-balance.sh "$f" "$out"
done
