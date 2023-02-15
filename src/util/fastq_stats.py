"""
Generates csv file of overview stats for a fastq file or directory of fastq files
"""
import argparse
import os
import gzip
import numpy as np
import pandas as pd
from Bio import SeqIO



def get_info(fastq:os.path, zipped:bool):
    """Gets basic information about fastq file and prints report

    Args:
        fastq (os.path): path to fastq file
        zipped (bool): .gz file or directory
    """
    if zipped:
        with gzip.open(fastq, "rt") as file:
            records = list(SeqIO.parse(file, "fastq"))
            num_reads = len(records)
    else:
        records = list(SeqIO.parse(fastq, "fastq"))
        num_reads = len(records)
    name = fastq.split('/')[-1]
    print(f'\nBASIC STATISTICS FOR {name}:')
    print(f'Number of Reads: {num_reads}')


    return num_reads

def parse_args():
    """parses fastq format
    """
    parser = argparse.ArgumentParser(
        description='Takes in fastq file and prints out base summary report')
    parser.add_argument('fastq', type=str, help='fastq file location')
    parser.add_argument('-d', '--directory',
                        action='store_true',
                        default=False,
                        help='Use a directory of fastq files (any .fastq file in the directory will be processed)')
    parser.add_argument('-o', '--output', type=str, default=None, help='Name of output file')
    parser.add_argument('--gz', action='store_true', help='Files are zipped (directory or file of fastq.gz filetype)')

    args = parser.parse_args()
    fastq = args.fastq
    fastq = '/mnt/lustre/hsm/nlsas/notape/home/uvi/be/posadalab/loretta/fastq/virome_fastq/'
    use_directory = args.directory
    output = args.output
    if output is None:
        output = 'fastq_overview'
    zipped = args.gz


    reads = []
    names = []

    if use_directory and os.path.exists(fastq):
        for fastq_path in os.listdir(fastq):
            search = '.fastq.gz' if zipped else '.fastq'
            if fastq_path.split(fastq_path.split('.')[0])[-1] == search:
                new_path = os.path.join(fastq, fastq_path)
                num_reads = get_info(new_path, zipped)
                reads.append(num_reads)
                names.append(fastq_path)
    elif not use_directory and os.path.exists(fastq):
        num_reads = get_info(fastq, zipped)
        reads.append(num_reads)
        names.append(fastq_path)
    else:
        print('Path does not exist, please enter a valid path')


    data_dict = {"Sample": names, 'NumberReads': reads}
    data = pd.DataFrame(data_dict)
    print(f'Mean reads: {np.mean(reads)}')
    print(f'Max reads: {np.max(reads)}')
    print(f'Min reads: {np.min(reads)}')
    print(f'Stdev reads: {np.std(reads)}')

    data.to_csv(f'../../data/output/{output}.csv')

if __name__=="__main__":
    parse_args()
