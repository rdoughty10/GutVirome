"""Initializes SeqScreen pipeline by creating necessary folders and other information
"""
import os
import argparse


def mkdir_p(directory:str):
    '''make directory if does not exist'''
    if not os.path.exists(directory):
        os.mkdir(directory)


def initialize(output:str, name:str):
    """Initializes folders 

    Args:
        output (str): location where pipeline files should be stored
        name (str): name of subdirectory containing files
    """
    ## create general output folder
    output_folder = os.path.join(output, name)
    mkdir_p(output_folder)

    ## create sub folders
    fastq_folder = os.path.join(output_folder, 'fastq')
    fastqc_folder = os.path.join(output_folder, 'fastqc')
    multiqc_folder = os.path.join(output_folder, 'multiqc')
    fastp_folder = os.path.join(output_folder, 'fastp')
    removed_human_folder = os.path.join(output_folder, 'removed-human')
    fasta_folder = os.path.join(output_folder, 'fasta')
    fasta_split_folder = os.path.join(output_folder, 'fasta-split')
    seqscreen_folder = os.path.join(output_folder, 'seqscreen')
    taxonkit_folder = os.path.join(output_folder, 'taxonkit')
    processing_folder = os.path.join(output_folder, 'output')
    unmapped_folder = os.path.join(output_folder, 'unmapped')
    unmapped_blast_folder = os.path.join(output_folder, 'unmapped_blast')

    mkdir_p(fastq_folder)
    mkdir_p(fastqc_folder)
    mkdir_p(multiqc_folder)
    mkdir_p(fastp_folder)
    mkdir_p(removed_human_folder)
    mkdir_p(seqscreen_folder)
    mkdir_p(fasta_folder)
    mkdir_p(fasta_split_folder)
    mkdir_p(taxonkit_folder)
    mkdir_p(processing_folder)
    mkdir_p(unmapped_folder)
    mkdir_p(unmapped_blast_folder)
    
    ## seqscreen, taxonkit, unmapped, unmapped_blast sub folders
    fast = os.path.join(seqscreen_folder, 'fast')
    sensitive = os.path.join(seqscreen_folder, 'sensitive')
    final = os.path.join(seqscreen_folder, 'final')
    mkdir_p(fast)
    mkdir_p(sensitive)
    mkdir_p(final)
    fast = os.path.join(taxonkit_folder, 'fast')
    sensitive = os.path.join(taxonkit_folder, 'sensitive')
    mkdir_p(fast)
    mkdir_p(sensitive)
    fast = os.path.join(unmapped_folder, 'fast')
    sensitive = os.path.join(unmapped_folder, 'sensitive')
    mkdir_p(fast)
    mkdir_p(sensitive)
    fast = os.path.join(unmapped_blast_folder, 'fast')
    sensitive = os.path.join(unmapped_blast_folder, 'sensitive')
    mkdir_p(fast)
    mkdir_p(sensitive)

def parse_args():
    """Parses arguments for script form
    """
    parser = argparse.ArgumentParser(description='Initializes SeqScreen Pipeline')
    parser.add_argument('output', type=str, help='Location where output folder should be')
    parser.add_argument('name', type=str, help='Name of batch folder')

    args = parser.parse_args()
    output = args.output
    batch_name = args.name

    initialize(output, batch_name)

if __name__=="__main__":
    parse_args()
