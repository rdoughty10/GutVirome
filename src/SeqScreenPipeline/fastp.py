"""Processes fastq files with fastp"""
import argparse
import os
import glob
from slurm import slurm


def fastp(pipeline:str, alt:str=None, alt_name:str=None):
    """Runs seqtk on the files for length and quality filtering

    Args:
        pipeline (str): pipeline files
        alt (str): alternative input 
    """
    if alt is None:
        fastq_dir = os.path.join(pipeline, 'fastq')
        input_files = glob.glob(f'{fastq_dir}/*1.fastq')
    else:
        fastq_dir = alt
        if alt_name is None:
            input_files = glob.glob(f'{fastq_dir}/*1.fastq')
        else:
            all_files = glob.glob(f'{fastq_dir}/{alt_name}')
            input_files = [file for file in all_files if '1.fastq' in file]
        
    fastp_dir = os.path.join(pipeline, 'fastp')

    ## get fastp commands
    for sample in input_files:
        filename = sample.split('/')[-1].split('1.fastq')[0]
        r1 = f'{filename}1.fastq'
        r2 = f'{filename}2.fastq'
        file_loc_r1 = os.path.join(fastq_dir, r1)
        file_loc_r2 = os.path.join(fastq_dir, r2)
        out_loc_r1 = os.path.join(fastp_dir, r1)
        out_loc_r2 = os.path.join(fastp_dir, r2)
        threads = 5
        if not (os.path.exists(out_loc_r1) and os.path.exists(out_loc_r2)):
            command = f'fastp -i {file_loc_r1} -I {file_loc_r2} -o {out_loc_r1} -O {out_loc_r2} -l 50 -y -3 -W 4 -M 20 -x --thread {threads}'
            slurm([command], f'{filename}_fastp', hours=1, days=0, memory=4, tasks=1, threads_per_task=threads) 
    
    #   If doing deduplication
    #   command = f'fastp -i {file_loc_r1} -I {file_loc_r2} -o {out_loc_r1} -O {out_loc_r2} -l 50 -y --dedup -W 4 -M 20 -x --thread {threads}'
    #   commands.append(command)
           


def parse_args():
    """Parses arguments for fastp
    """
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastq files with fastp')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing files')
    parser.add_argument('--alt-input', type=str, default=None, help='location if fastq folders are in different location')
    parser.add_argument('--alt-name', type=str, default=None, help='general name format for alt input folder fastq files')

    args = parser.parse_args()
    pipeline = args.pipeline
    alt = args.alt_input
    name = args.alt_name

    fastp(pipeline, alt, name)

if __name__=="__main__":
    parse_args()
