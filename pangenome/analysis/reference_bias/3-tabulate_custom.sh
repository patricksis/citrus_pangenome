#!/bin/bash -e

echo -e "library\taligner\tmean\tstderr" > ../out/alt_freq_stats.tsv

while read library_id; do
  for aligner in linear pan; do
    file="../2_calc-allele-balance/${aligner}/${library_id}_${aligner}.tsv"
    mean=$(awk '{x+=$6} END {print x/NR}' "$file")
    stdev=$(awk -v mean=$mean '{s+=($6-mean)^2} END {print sqrt(s/NR)/sqrt(NR)}' "$file")
    echo -e "$library_id\t$aligner\t$mean\t$stdev"
  done
done < library_ids.txt >> ../out/alt_freq_stats.tsv
