"""Parses results and processes of seqscreen pipeline and gives full table"""
import argparse
import os
import pandas as pd
import numpy as np
from collections import Counter



def get_tax_counts(viral_ranks, viral, level='species'):
    """Generates unique list and counts of number of reads at certain level given viral ranks list and full taxonkit output

    Args:
        viral_ranks (_type_): supporting dataframe containing lineage of each assigned read
        viral (_type_): taxonkit output filtered for viruses
        level (str, optional): rank to search for (species, genus, family, phylum, etc). Defaults to 'species'.

    Returns:
        the number of unique viruses, the total reads with information at that level, and a dataframe of the virus and their counts
    """
    
    
    assignments = Counter()

    for index, row in viral_ranks.iterrows():
        try:
            col = list(row).index(level)
            assignment = viral.loc[index, col]
            assignments.update([assignment])
        except:
            col = None
            assignment = None
    
    assignments = dict(assignments)

    # assigned_virus = viral.lookup(species_cols.index, species_cols.values)
    counts = list(assignments.values())
    unique_viruses = len(assignments)
    return unique_viruses, np.sum(counts), assignments



def clean_count_data(data:list, files:list):
    """Cleans the taxa information and returns list

    Args:
        data (list): data
        files (list): files

    Returns:
        _type_: taxonomy data
    """
    print(data)
    print(files)
    
    ## get unique taxa across all samples
    taxa = []
    for sample in data:
       taxa.append(list(sample.keys()))
    taxa = list(set([tax for sublist in taxa for tax in sublist]))

    ## create dataframe with columns of taxa
    taxon_data = pd.DataFrame(columns=taxa)

    ## add counts for each sample
    for sample, filename in zip(data, files):
        row = pd.Series(sample, name=filename)
        taxon_data = pd.concat([taxon_data, pd.DataFrame([row])])
        
    print(taxon_data)
        
    return taxon_data.transpose()
    

def last_non_na(row):
    last_valid_index = row.last_valid_index()
    if last_valid_index is not None:
        return row[last_valid_index]
    else:
        return None

def seqscreen_metrics(file:str):
    """Generates seqscreen metrics and other data given a taxonkit output file

    Args:
        file (str): taxoknkit output file

    Returns:
        data
    """
    print(f'Processing {file}')
    data = pd.read_csv(file, delimiter='\t')

    ## base statistics (reads, assigned reads overall, percentage assigned)
    total_reads = len(data)
    assigned = data.dropna()
    total_assigned_reads = len(assigned)
    assigned_percent = np.round(total_assigned_reads/total_reads * 100, 2)

    ##parse the taxonkit outputs into own tables
    split = assigned.iloc[:, -2].str.split(";", expand=True)
    ranks = assigned.iloc[:, -1].str.split(";", expand=True)
    
    ## get base bacterial information and number of reads (# bacterial reads, percent bacterial reads assigned)
    bacteria = split[split[1] =='Bacteria']
    bacteria_reads = len(bacteria)
    reads_percent_bacteria = np.round(bacteria_reads/total_assigned_reads * 100, 2)

    ## get base viral information and number of reads (# viral reads, percent viral reads assigned)
    viral = split[split[0] =='Viruses']
    viral_ranks = ranks[split[0] == 'Viruses']
    viral_reads = len(viral)
    reads_percent_viral = np.round(viral_reads/total_assigned_reads * 100, 2)
    viral_cop = viral
    
    ## get the assigned values for each viral assignment and number of unique assignments 
    # (# unique assignments, list and count of each)
    viral['assignment'] = viral.apply(last_non_na, axis=1)
    # assigned_tax_col = viral.apply(pd.Series.last_valid_index, axis=1)
    # assigned_virus = viral.lookup(assigned_tax_col.index, assigned_tax_col.values)
    virus, counts = np.unique(viral['assignment'], return_counts=True)
    unique_assignments = len(virus)
    virus_counts = {vir: count for vir, count in zip(virus, counts)}

    ##get the species values for each assignment
    # print(file)
    unique_species, total_species_assignments, virus_species_counts = get_tax_counts(viral_ranks,
                                                                                 viral_cop,
                                                                                 level='species')
    unique_genuses, total_genus_assignments, virus_genus_counts = get_tax_counts(viral_ranks,
                                                                                 viral_cop,
                                                                                 level='genus')
    unique_families, total_family_assignments, virus_family_counts = get_tax_counts(viral_ranks,
                                                                                    viral_cop,
                                                                                    level='family')

    ## aggregate data
    output_base_data = [file.split('/')[-1].split('.tsv')[0],
                   total_reads,
                   total_assigned_reads,
                   assigned_percent,
                   bacteria_reads,
                   reads_percent_bacteria,
                   viral_reads,
                   reads_percent_viral,
                   unique_assignments,
                   unique_species,
                   total_species_assignments,
                   unique_genuses,
                   total_genus_assignments,
                   unique_families,
                   total_family_assignments]
    
    output_labels = ['filename',
                   'total_reads',
                   'total_assigned_reads',
                   'assigned_percent',
                   'bacteria_reads',
                   'reads_percent_bacteria',
                   'viral_reads',
                   'reads_percent_viral',
                   'unique_assignments',
                   'unique_species',
                   'total_species_assignments',
                   'unique_genuses',
                   'total_genus_assignments',
                   'unique_families',
                   'total_family_assignments']

    counts = {'assigned': virus_counts,
              'species': virus_species_counts,
              'genus': virus_genus_counts,
              'family': virus_family_counts}

    return (output_base_data, output_labels), counts


def get_unmapped_data(file:str, database:str):
    
    ## import data
    columns = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qlen', 'qstart', 'qend', 'slen', 'sstart', 'send', 'evalue', 'bitscore']
    data = pd.read_csv(file, delimiter='\t', header=None, names=columns)

    if database=='mgv':
        metadata = pd.read_csv('../ViromeDatabaseAnalysis/metadata/mgv_contig_info.tsv', delimiter='\t')
    if database=='gpd':
        metadata = pd.read_csv('../ViromeDatabaseAnalysis/metadata/GPD_metadata.tsv', delimiter='\t')
        
    new_reads_with_hits = len(np.unique(data['qseqid']))
    avg_hits_per_read = len(data) / new_reads_with_hits
    number_unique_contigs = len(np.unique(data['sseqid']))
    avg_reads_per_contig = len(data) / number_unique_contigs
    
    overview_data = [new_reads_with_hits, avg_hits_per_read, number_unique_contigs, avg_reads_per_contig]
    overview_labels = [f'[{database}] Unmapped reads with hits', f'[{database}] Hits per read', f'[{database}] Number of contigs with hits', f'[{database}] Reads per contig']
        
    
    
    return (overview_data, overview_labels), 1
    


def get_results(pipeline:str, sensitive:bool):
    """Aggregates results of taxonkit from seqscreen and provides a nice table

    Args:
        pipeline (str): _description_
        sensitive (bool): _description_
    """
    if sensitive:
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'sensitive')
        #unmapped_data = os.path.join(pipeline, 'unmapped_blast', 'sensitive')
    else:
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'fast', 'final')
        #unmapped_data = os.path.join(pipeline, 'unmapped_blast', 'fast')
    # taxonkit_dir = pipeline
    # unmapped_blast_reports = os.listdir(unmapped_data)
    # unmapped_blast_search = len(unmapped_blast_reports) > 0

    print(taxonkit_dir)
    files = os.listdir(taxonkit_dir)
    files = sorted(files)

    main_data = []
    main_labels = []
    
    assignment_data = []
    species_data = []
    genus_data = []
    family_data = []
    
    
    
    for taxonkit_file in files:
        file_loc = os.path.join(taxonkit_dir, taxonkit_file)

        ## get information for that particular output
        (seqscreen_data, seqscreen_labels), tax_counts = seqscreen_metrics(file_loc)
        
        ## get information for unmapped reads database output if it exist
        # if unmapped_blast_search:
        #     base_file_name = taxonkit_file.split('.tsv')[0]
        #     gpd = os.path.join(unmapped_data, f'{base_file_name}.fastaxGPD.tsv')
        #     mgv = os.path.join(unmapped_data, f'{base_file_name}.fastaxMGV.tsv')
            
        #     (gpd_overview, gpd_labels), gpd_data = get_unmapped_data(gpd, 'gpd')
        #     (mgv_overview, mgv_labels), mgv_data = get_unmapped_data(mgv, 'mgv')
            
        #     seqscreen_data.extend(gpd_overview)
        #     seqscreen_data.extend(mgv_overview)
            
        #     seqscreen_labels.extend(gpd_labels)
        #     seqscreen_labels.extend(mgv_labels)
            
        
        main_data.append(seqscreen_data)
        main_labels.append(seqscreen_labels)
        
        assignment_data.append(tax_counts['assigned'])
        species_data.append(tax_counts['species'])
        genus_data.append(tax_counts['genus'])
        family_data.append(tax_counts['family'])
        
    main_labels = main_labels[0]
    
    
    ## create the overview file from seqscreen_data outputs for each file
    output = pd.DataFrame(main_data, columns=main_labels)
    output_loc = os.path.join(pipeline, 'output', 'fast_output.csv')
    output.to_csv(output_loc)


    assignment_data = clean_count_data(assignment_data, files)
    species_data = clean_count_data(species_data, files)
    genus_data = clean_count_data(genus_data, files)
    family_data = clean_count_data(family_data, files)

    assignment_data.to_csv(os.path.join(pipeline, 'output', 'assignment_data.csv'))
    species_data.to_csv(os.path.join(pipeline, 'output', 'species_data.csv'))
    genus_data.to_csv(os.path.join(pipeline, 'output', 'genus_data.csv'))
    family_data.to_csv(os.path.join(pipeline, 'output', 'family_data.csv'))


     
    


def parse_args():
    """Parses args for command
    """
    parser = argparse.ArgumentParser(description='Gives results in human readable format')
    parser.add_argument('pipeline', type=str, help='Location of pipeline files')
    parser.add_argument('-s', '--sensitive',
                        action='store_true',
                        default=False,
                        help='Process sensitive mode files')

    args = parser.parse_args()
    pipeline = args.pipeline
    sensitive = args.sensitive

    get_results(pipeline, sensitive)

if __name__=="__main__":
    parse_args()
