grep "^W" citrus-pg-full_renamed.gfa | cut -f2 | sort | uniq | while read genome; do
    GFF_FILE="gff/${genome}_NLR_merged_sorted_v2.gff3"
    OUTDIR="grannot_results/$genome"
        grannot citrus-pg-full_renamed.gfa "$GFF_FILE" "$genome" --annotation --pav_matrix --outdir "$OUTDIR"
    else
        echo "No GFF found for $genome ($GFF_FILE), skipping..."
    fi
done
