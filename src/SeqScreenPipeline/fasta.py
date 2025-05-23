"""
converts fastq files to fasta files with seqtk 
"""
import argparse
import os
import glob
from slurm import slurm


def fasta(pipeline:str):
    """Runs seqtk on the files to convert to fasta

    Args:
        pipeline (str): _description_
    """
    removed_human_dir = os.path.join(pipeline, 'removed-human')
    fasta_dir = os.path.join(pipeline, 'fasta')
    
    input_files = glob.glob(f'{removed_human_dir}/*.fastq')

    ## process with seqtk
    i = 1
    for file in input_files:
        name = file.split('/')[-1]
        fasta_name = name[:-1] + 'a'
        out_loc = os.path.join(fasta_dir, fasta_name)
        if not os.path.exists(out_loc):
            command = f'seqtk seq -A {file} > {out_loc}'
            print(f'[{i}]{command}')
            i+=1
            name = out_loc.split('/')[-1]
            slurm([command], f'{name}_fasta', hours=1, days=0, memory=16)



def parse_args():
    """Parses arguments for fasta conversion 
    """
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastq files into fasta')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing fastq files')

    args = parser.parse_args()
    pipeline = args.pipeline

    fasta(pipeline)

if __name__=="__main__":
    parse_args()
