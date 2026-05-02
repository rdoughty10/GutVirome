import os
import pandas as pd
from glob import glob
from collections import defaultdict

indir = "/mnt/lustre/hsm/nlsas/notape/home/uvi/be/posadalab/loretta/Methods_Comparison_Data/taxonkit/fast/final"
outdir = "/mnt/lustre/hsm/nlsas/notape/home/uvi/be/posadalab/loretta/Methods_Comparison_Data/output"
os.makedirs(outdir, exist_ok=True)

# ranks we extract (skip domain)
rank_prefixes = {
    "phylum": "p__",
    "class": "c__",
    "order": "o__",
    "family": "f__",
    "genus": "g__",
    "species": "s__"
}

# collectors for rank-count matrices
rank_tables = {r: defaultdict(int) for r in rank_prefixes}

overview_rows = []

tsv_files = glob(os.path.join(indir, "*.tsv"))

for i, f in enumerate(tsv_files):
    
    print(f"Processed file {i}:{f}")
    sample = os.path.basename(f).replace(".tsv", "")

    df = pd.read_csv(f,
                     sep="\t",
                     header=None,
                     names=["idx", "query", "lca", "taxonomy"],
                     dtype=str,
                     engine="python",
                     keep_default_na=False)
    
    # --- overview fields ---
    total_reads = len(df)
    assigned_reads = (df['lca'] != "-").sum()

    assigned_tax = df['taxonomy'].fillna("-")
    viral_reads = assigned_tax.str.startswith("d__Viruses").sum()
    bacterial_reads = assigned_tax.str.startswith("d__Bacteria").sum()

    overview_rows.append({
        "sample": sample,
        "total_reads": total_reads,
        "assigned_reads": assigned_reads,
        "assigned_viral_reads": viral_reads,
        "assigned_bacterial_reads": bacterial_reads
    })

    # --- rank counting ---
    viral_only = assigned_tax[
        (assigned_tax != "-") &
        (assigned_tax.str.startswith("d__Viruses"))
    ]


    for tax in viral_only:
        parts = tax.split(";")
        extracted = {rank: None for rank in rank_prefixes}

        for part in parts:
            for rank, prefix in rank_prefixes.items():
                if part.startswith(prefix):
                    extracted[rank] = part[len(prefix):]

        for rank, val in extracted.items():
            if val not in (None, "unclassified", ""):
                rank_tables[rank][(val, sample)] += 1

# --- write overview ---
pd.DataFrame(overview_rows).to_csv(
    os.path.join(outdir, "overview.tsv"), sep="\t", index=False
)

# --- write rank matrices ---
for rank in rank_prefixes:
    entries = rank_tables[rank]

    # unique taxa and samples
    taxa = sorted({t for (t, s) in entries.keys()})
    samples = sorted({s for (t, s) in entries.keys()})

    matrix = pd.DataFrame(0, index=taxa, columns=samples)

    for (taxon, sample), count in entries.items():
        matrix.at[taxon, sample] = count

    matrix.to_csv(
        os.path.join(outdir, f"{rank}.tsv"),
        sep="\t"
    )
