"""
Parses and processes the output of the SeqScreen pipeline,
producing summary statistics and detailed taxonomic assignments for viral data.
"""

import argparse
import os
import pandas as pd
import numpy as np
from collections import Counter


def get_tax_counts(ranks_df, viral_df, level='species'):
    """
    Calculates counts of viral assignments at a given taxonomic level.
    """
    counts = Counter()
    for idx, rank_row in ranks_df.iterrows():
        try:
            col_index = list(rank_row).index(level)
            assignment = viral_df.loc[idx, col_index]
        except:
            assignment = 'Not Classified'
        counts.update([assignment])

    return len(counts), sum(counts.values()), dict(counts)


def clean_count_data(data_list, file_names):
    taxa = list(set(taxon for sample in data_list for taxon in sample.keys()))
    taxon_df = pd.DataFrame(columns=taxa)

    for sample, name in zip(data_list, file_names):
        sample_series = pd.Series(sample, name=name)
        taxon_df = pd.concat([taxon_df, pd.DataFrame([sample_series])])

    return taxon_df.transpose()


def abbreviate(rank):
    abbr = {
        'superkingdom': 'sk', 'domain': 'do', 'kingdom': 'ki', 'phylum': 'ph',
        'class': 'cl', 'order': 'or', 'family': 'fa', 'genus': 'ge', 'species': 'sp',
        'subkingdom': 'skg', 'subphylum': 'sph', 'subclass': 'scl', 'infraorder': 'io',
        'subfamily': 'sfa', 'subgenus': 'sge', 'parvorder': 'po', 'section': 'se',
        'clade': 'cld', 'no rank': 'nr', 'strain': 'st', 'morph': 'mo', 'forma specialis': 'fs'
    }
    return abbr.get(rank.strip().lower(), rank[:2])


def combine_row(row):
    taxa = row[-2].split(';')
    ranks = row[-1].split(';')
    return ';'.join(f"{abbreviate(r)}_{t}" for r, t in zip(ranks, taxa))


def seqscreen_metrics(file_path):
    df = pd.read_csv(file_path, sep='\t')
    total_reads = len(df)
    assigned_df = df.dropna()
    total_assigned = len(assigned_df)
    pct_assigned = round(total_assigned / total_reads * 100, 2)

    split = assigned_df.iloc[:, -2].str.split(';', expand=True)
    ranks = assigned_df.iloc[:, -1].str.split(';', expand=True)

    bacteria_reads = len(split[split[1] == 'Bacteria'])
    pct_bacteria = round(bacteria_reads / total_assigned * 100, 2)

    viral_filter = split[0] == 'Viruses'
    viral_split = split[viral_filter].copy()
    viral_ranks = ranks[viral_filter]
    viral_assigned_df = assigned_df[viral_filter]
    viral_reads = len(viral_split)
    pct_viral = round(viral_reads / total_assigned * 100, 2)

    viral_split['assignment'] = viral_assigned_df.apply(combine_row, axis=1)
    unique_assignments, assignment_counts = np.unique(viral_split['assignment'], return_counts=True)
    assignment_summary = dict(zip(unique_assignments, assignment_counts))

    species_u, species_n, species_counts = get_tax_counts(viral_ranks, viral_split, 'species')
    genus_u, genus_n, genus_counts = get_tax_counts(viral_ranks, viral_split, 'genus')
    family_u, family_n, family_counts = get_tax_counts(viral_ranks, viral_split, 'family')
    order_u, order_n, order_counts = get_tax_counts(viral_ranks, viral_split, 'order')
    class_u, class_n, class_counts = get_tax_counts(viral_ranks, viral_split, 'class')

    base_data = [
        os.path.basename(file_path).replace('.tsv', ''), total_reads, total_assigned, pct_assigned,
        bacteria_reads, pct_bacteria, viral_reads, pct_viral, len(unique_assignments),
        species_u, species_n, genus_u, genus_n, family_u, family_n, order_u, order_n, class_u, class_n
    ]

    labels = [
        'filename', 'total_reads', 'total_assigned_reads', 'assigned_percent',
        'bacteria_reads', 'reads_percent_bacteria', 'viral_reads', 'reads_percent_viral',
        'unique_assignments', 'unique_species', 'total_species_assignments',
        'unique_genuses', 'total_genus_assignments', 'unique_families', 'total_family_assignments',
        'unique_order', 'total_order_assignments', 'unique_class', 'total_class_assignments'
    ]

    counts = {
        'assigned': assignment_summary,
        'species': species_counts,
        'genus': genus_counts,
        'family': family_counts,
        'order': order_counts,
        'class': class_counts
    }

    return (base_data, labels), counts


def get_results(pipeline_dir, sensitive_mode):
    mode_dir = 'sensitive' if sensitive_mode else os.path.join('fast', 'final')
    taxonkit_path = os.path.join(pipeline_dir, 'taxonkit', mode_dir)
    os.makedirs(os.path.join(pipeline_dir, 'output'), exist_ok=True)

    summary_data, summary_labels = [], []
    tax_data = {k: [] for k in ['assigned', 'species', 'genus', 'family', 'order', 'class']}

    taxonkit_files = sorted(os.listdir(taxonkit_path))
    for file_name in taxonkit_files:
        full_path = os.path.join(taxonkit_path, file_name)
        (data_row, labels), count_data = seqscreen_metrics(full_path)

        summary_data.append(data_row)
        summary_labels = labels
        for level in tax_data:
            tax_data[level].append(count_data[level])

    pd.DataFrame(summary_data, columns=summary_labels).to_csv(os.path.join(pipeline_dir, 'output', 'fast_output.csv'))

    for level, counts in tax_data.items():
        clean_count_data(counts, taxonkit_files).to_csv(os.path.join(pipeline_dir, 'output', f'{level}_data.csv'))


def parse_args():
    parser = argparse.ArgumentParser(description='Summarize SeqScreen taxonomic outputs')
    parser.add_argument('pipeline', type=str, help='Path to pipeline output directory')
    parser.add_argument('-s', '--sensitive', action='store_true', help='Use sensitive mode output')
    args = parser.parse_args()
    get_results(args.pipeline, args.sensitive)


if __name__ == "__main__":
    parse_args()