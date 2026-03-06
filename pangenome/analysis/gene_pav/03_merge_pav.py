mport pandas as pd
import glob

# Step 1: Grab all cleaned PAV files
pav_files = glob.glob("c_*_PAV.txt")

# Step 2: Load each file into a list
df_list = [pd.read_csv(file, sep="\t") for file in pav_files]

# Step 3: Stack all genes from all files
merged = pd.concat(df_list, ignore_index=True)

# Step 4: Fill missing values (e.g., gene not present in some genomes)
merged.fillna(0, inplace=True)

# Step 5: Make sure PAV calls are 0/1 integers
merged.iloc[:, 1:] = merged.iloc[:, 1:].astype(int)

# Step 6: Save to a file
merged.to_csv("merged_pav_matrix.tsv", sep="\t", index=False)

print("Merged matrix saved to 'merged_pav_matrix.tsv'")
