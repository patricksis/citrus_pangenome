#!/usr/bin/env python3
# Identify regions of the reference backbone that a haplotype's walks do not
# cover in the clipped pangenome graph, and report them in reference coordinates.
# For each haplotype walk file, find the first and last backbone nodes it
# traverses, merge those covered spans, and subtract them from the full
# backbone span. The remaining gaps are the clipped regions (BED output).

import re, glob, pandas as pd

# loop over every backbone scaffold file
for backbone_path in sorted(glob.glob("../../walk_files/c_reticulata_fortune_primary#0#Scaffold_*.tsv")):
    msc = re.search(r"(Scaffold_\d+)", backbone_path)
    if not msc: 
        continue
    scaffold = msc.group(1)
    hap_glob = f"../../walk_files/c_australis#1#{scaffold}_*.tsv"
    out_bed  = f"australis1.{scaffold}.clips.bed"

    # 1) Load backbone 
    bdf = pd.read_csv(backbone_path, sep="\t")

    

    # Ordered list of backbone nodes
    B_list = bdf["node"].tolist()

    # Set for fast membership checks
    B_set = set()
    for n in B_list:
        B_set.add(n)

    # Index map node -> backbone index
    B_idx = {}
    for i, n in enumerate(B_list):
        B_idx[n] = i
    print("Backbone index map sample:", list(B_idx.items())[:5])

    # 2) Gather & sort hap files
    rx = re.compile(r".*_(\d+)-(\d+)\.tsv$")
    hap_files = []
    for p in glob.glob(hap_glob):
        m = rx.match(p)
        if m is None:
            continue
        start_num = int(m.group(1))
        hap_files.append((start_num, p))
    hap_files.sort(key=lambda x: x[0])
    ordered_files = []
    for _, p in hap_files:
        ordered_files.append(p)

    # 3) Build covered spans per file (first/last backbone node)
    covered_spans = []
    for p in ordered_files:
        df = pd.read_csv(p, sep="\t", usecols=["chr","start","end","node"])
        df = df.sort_values(["start","end"]).reset_index(drop=True)
        nodes = df["node"].tolist()

        i_first = None
        for n in nodes:
            if n in B_set:
                i_first = B_idx[n]
                break

        i_last = None
        for n in reversed(nodes):
            if n in B_set:
                i_last = B_idx[n]
                break

        if i_first is None or i_last is None:
            continue
        if i_first > i_last:
            tmp = i_first; i_first = i_last; i_last = tmp

        chr_ = bdf.loc[i_first, "chr"]
        s    = int(bdf.loc[i_first, "start"])
        e    = int(bdf.loc[i_last,  "end"])
        covered_spans.append((chr_, s, e))

    # 4) Merge covered spans
    covered_spans.sort(key=lambda x: (x[0], x[1], x[2]))
    merged = []
    for chr_, s, e in covered_spans:
        if len(merged) == 0:
            merged.append([chr_, s, e])
            continue
        last_chr, last_s, last_e = merged[-1]
        if chr_ != last_chr or s > last_e:
            merged.append([chr_, s, e])
        else:
            if e > last_e:
                merged[-1][2] = e

    # 5) Subtract from backbone span to get clips
    BB_chr  = str(bdf.iloc[0]["chr"])
    BB_span_start = int(bdf.iloc[0]["start"])
    BB_span_end   = int(bdf.iloc[len(bdf)-1]["end"])

    cov = []
    for chr_, s, e in merged:
        if chr_ == BB_chr:
            cov.append((s, e))
    cov.sort(key=lambda x: (x[0], x[1]))

    clips = []
    cur = BB_span_start
    for s, e in cov:
        if e <= cur:
            continue
        if s > cur:
            gap_start = cur
            gap_end = min(s, BB_span_end)
            if gap_end > gap_start:
                clips.append((BB_chr, gap_start, gap_end))
        if e > cur:
            cur = e
        if cur >= BB_span_end:
            break
    if cur < BB_span_end:
        clips.append((BB_chr, cur, BB_span_end))

    # filter small gaps (set to 0 to keep all)
    MIN_BP = 0
    filtered_clips = []
    for chr_, s, e in clips:
        if (e - s) >= MIN_BP:
            filtered_clips.append((chr_, s, e))

    # Write to file
    with open(out_bed, "w") as w:
        for chr_, s, e in filtered_clips:
            w.write(f"{chr_}\t{s}\t{e}\n")

    print("processed", scaffold,
          "hap files read:", len(ordered_files),
          "covered_spans:", len(covered_spans),
          "merged spans:", len(merged),
          "clips total:", len(filtered_clips),
          "wrote:", out_bed)
