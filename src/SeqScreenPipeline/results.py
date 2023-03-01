"""Parses results and processes of seqscreen pipeline and gives full table"""
import argparse
import os
import pandas as pd
import numpy as np


def get_tax_counts(viral_ranks, viral, level='species'):
    """Generates unique list and counts of number of reads at certain level given viral ranks list and full taxonkit output

    Args:
        viral_ranks (_type_): supporting dataframe containing lineage of each assigned read
        viral (_type_): taxonkit output filtered for viruses
        level (str, optional): rank to search for (species, genus, family, phylum, etc). Defaults to 'species'.

    Returns:
        the number of unique viruses, the total reads with information at that level, and a dataframe of the virus and their counts
    """
    species_cols = []
    for index, row in viral_ranks.iterrows():
        try:
            col = list(row).index(level)
        except:
            col = None
        species_cols.append([index, col])
    species_cols = pd.DataFrame(np.array(species_cols), columns=['index', 'col']).dropna().set_index('index').squeeze()
    assigned_virus = viral.lookup(species_cols.index, species_cols.values)
    virus, counts = np.unique(assigned_virus, return_counts=True)
    unique_viruses = len(virus)
    virus_counts = {vir: count for vir, count in zip(virus, counts)}
    return unique_viruses, np.sum(counts), virus_counts


def clean_count_data(data:list, files:list):

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
        taxon_data = taxon_data.append(row)
        
    return taxon_data.transpose()
    



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
    split = assigned['Unnamed: 44'].str.split(";", expand=True)
    ranks = assigned['Unnamed: 45'].str.split(";", expand=True)

    ## get base viral information and number of reads (# viral reads, percent viral reads assigned)
    viral = split[split[0] =='Viruses']
    viral_ranks = ranks[split[0] == 'Viruses']
    viral_reads = len(viral)
    reads_percent_viral = np.round(viral_reads/total_assigned_reads * 100, 2)

    ## get the assigned values for each viral assignment and number of unique assignments 
    # (# unique assignments, list and count of each)
    assigned_tax_col = viral.apply(pd.Series.last_valid_index, axis=1)
    assigned_virus = viral.lookup(assigned_tax_col.index, assigned_tax_col.values)
    virus, counts = np.unique(assigned_virus, return_counts=True)
    unique_assignments = len(virus)
    virus_counts = {vir: count for vir, count in zip(virus, counts)}

    ##get the species values for each assignment
    unique_species, total_species_assignments, virus_species_counts = get_tax_counts(viral_ranks,
                                                                                 viral,
                                                                                 level='species')
    unique_genuses, total_genus_assignments, virus_genus_counts = get_tax_counts(viral_ranks,
                                                                                 viral,
                                                                                 level='genus')
    unique_families, total_family_assignments, virus_family_counts = get_tax_counts(viral_ranks,
                                                                                    viral,
                                                                                    level='family')

    ## aggregate data
    output_base_data = [file.split('/')[-1].split('.tsv')[0],
                   total_reads,
                   total_assigned_reads,
                   assigned_percent,
                   viral_reads,
                   reads_percent_viral,
                   unique_assignments,
                   unique_species,
                   total_species_assignments,
                   unique_genuses,
                   total_genus_assignments,
                   unique_families,
                   total_family_assignments]

    counts = {'assigned': virus_counts,
              'species': virus_species_counts,
              'genus': virus_genus_counts,
              'family': virus_family_counts}

    return output_base_data, counts



def get_results(pipeline:str, sensitive:bool):
    """Aggregates results of taxonkit from seqscreen and provides a nice table

    Args:
        pipeline (str): _description_
        sensitive (bool): _description_
    """
    if sensitive:
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'sensitive')
    else:
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'fast')

    files = os.listdir(taxonkit_dir)

    main_data = []
    assignment_data = []
    species_data = []
    genus_data = []
    family_data = []
    
    
    for taxonkit_file in files:
        file_loc = os.path.join(taxonkit_dir, taxonkit_file)

        ## get information for that particular output
        seqscreen_data, tax_counts = seqscreen_metrics(file_loc)
        main_data.append(seqscreen_data)
        
        assignment_data.append(tax_counts['assigned'])
        species_data.append(tax_counts['species'])
        genus_data.append(tax_counts['genus'])
        family_data.append(tax_counts['family'])

    ## create the overview file from seqscreen_data outputs for each file
    output = pd.DataFrame(main_data, columns=['filename',
                   'total_reads',
                   'total_assigned_reads',
                   'assigned_percent',
                   'viral_reads',
                   'reads_percent_viral',
                   'unique_assignments',
                   'unique_species',
                   'total_species_assignments',
                   'unique_genuses',
                   'total_genus_assignments',
                   'unique_families',
                   'total_family_assignments'])
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