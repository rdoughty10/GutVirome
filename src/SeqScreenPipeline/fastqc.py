"""
Runs fastqc on bulk fastq files
"""
import argparse
import os
import slurm


def fastqc(pipeline:str):
    """Runs fastqc on the files

    Args:
        pipeline (str): _description_
    """
    fastq_dir = os.path.join(pipeline, 'fastq')
    fastqc_dir = os.path.join(pipeline, 'fastqc')

    input_files = os.listdir(fastq_dir)
    input_files = [os.path.join(fastq_dir, file) for file in input_files]

    ## process with fastqc
    command = f'fastqc -f fastq -o {fastqc_dir} -t 32 {" ".join(input_files)}'
    name = pipeline.split('/')[0]
    slurm.slurm_job(command, f'{name}_fastqc', hours=12, days=0, memory=16)



def parse_args():
    """Parses arguments for fastqc 
    """
    parser = argparse.ArgumentParser(description='Bulk processes folder of files with fastqc')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing fastq files')

    args = parser.parse_args()
    pipeline = args.pipeline

    fastqc(pipeline)

if __name__=="__main__":
    parse_args()
