import pandas as pd
import glob
import os

pav_files = glob.glob("c_*_PAV.txt")

for file in pav_files:
    df = pd.read_csv(file, sep="\t")

    # Extract genome name from the file
    genome = os.path.basename(file).replace("_PAV.txt", "")

    # Rename gene_id to include the genome name
    df['gene_id'] = df['gene_id'].apply(lambda x: f"{genome}_{x}")

    # Add self-genome column if missing
    if genome not in df.columns:
        print(f"Adding self column: {genome}")
        df[genome] = 1

    # Save back (overwrite original)
    df.to_csv(file, sep="\t", index=False)
