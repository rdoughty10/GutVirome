"""
Runs fastqc on bulk fastq files
"""
import argparse
import os
import glob
from slurm import slurm


def fastqc(pipeline:str, alt:str=None):
    """Runs fastqc on the files

    Args:
        pipeline (str): _description_
    """
    
    ## input directories
    if alt is None:
        fastq_dir = os.path.join(pipeline, 'fastq')
    else:
        fastq_dir = alt
    fastp_dir = os.path.join(pipeline, 'fastp')
    no_human_dir = os.path.join(pipeline, 'removed-human')
    
    ## output directories
    fastqc_dir_raw = os.path.join(pipeline, 'fastqc', 'raw')
    fastqc_dir_fastp = os.path.join(pipeline, 'fastqc', 'fastp')
    fastqc_dir_no_human = os.path.join(pipeline, 'fastqc', 'removed-human')

    ## get input files
    input_files_fastq = os.listdir(fastq_dir)
    input_files_fastq = [os.path.join(fastq_dir, file) for file in input_files_fastq]
    input_files_fastp = os.listdir(fastp_dir)
    input_files_fastp = [os.path.join(fastp_dir, file) for file in input_files_fastp]
    input_files_no_human = os.listdir(no_human_dir)
    input_files_no_human = [os.path.join(no_human_dir, file) for file in input_files_no_human]
    

    ## process with fastqc for before and after
    threads = 5
    command1 = f'fastqc -f fastq -o {fastqc_dir_raw} -t {threads} {" ".join(input_files_fastq)}'
    command2 = f'fastqc -f fastq -o {fastqc_dir_fastp} -t {threads} {" ".join(input_files_fastp)}'
    command3 = f'fastqc -f fastq -o {fastqc_dir_no_human} -t {threads} {" ".join(input_files_no_human)}'
    slurm([command1, command2, command3], 'fastqc', hours=1, days=0, memory=10, threads_per_task=threads)



def parse_args():
    """Parses arguments for fastqc 
    """
    parser = argparse.ArgumentParser(description='Bulk processes folder of files with fastqc')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing files')
    parser.add_argument('--alt-input', type=str, default=None, help='location if fastq folders are in different location')

    args = parser.parse_args()
    pipeline = args.pipeline
    alt = args.alt_input

    fastqc(pipeline, alt)

if __name__=="__main__":
    parse_args()
