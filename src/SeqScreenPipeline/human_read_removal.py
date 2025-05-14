'''Does human read removal using bowtie 2'''
import argparse
import os
import glob
from slurm import slurm


def remove_human(pipeline:str, genome:str, threads:int=1, paired=True):
    
    fastp_dir = os.path.join(pipeline, 'fastp')
    removed_reads = os.path.join(pipeline, 'removed-human')
    
    
    if paired:
        input_files = glob.glob(f'{fastp_dir}/*1.fastq')
        
        for file in input_files:
    
            ## if paired end reads not merged
            name = file.split('/')[-1].split('1.fastq')[0]
            r1 = f'{name}1.fastq'
            r2 = f'{name}2.fastq'
            r1_loc = os.path.join(fastp_dir, r1)
            r2_loc = os.path.join(fastp_dir, r2)
            out = os.path.join(removed_reads, name)
            command = f'bowtie2 -p {threads} -x {genome} -1 {r1_loc} -2 {r2_loc} --un-conc {out}'
            out_parts = out.split('/')[-1]
            out1 = os.path.join(removed_reads, f'{out_parts}.1')
            out2 = os.path.join(removed_reads, f'{out_parts}.2')
            mv_1 = f'mv {out1} {out}1.fastq'
            mv_2 = f'mv {out2} {out}2.fastq'
            
            if not os.path.exists(f'{out}_R1.fastq'):
                slurm([command, mv_1, mv_2], f'{name}_remove_human', hours=1, days=0, memory=10, threads_per_task=threads)

def parse_args():
    '''
    Parses arguments for command line function
    '''
    parser = argparse.ArgumentParser(description='Removes human reads from filtered samples')
    parser.add_argument('pipeline', type=str, help="location of pipeline files")
    parser.add_argument('genome', type=str, help="Location of bowtie indexes (note: probably in form GRCh38_noalt_as/GRCh38_noalt_as)")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    
    args = parser.parse_args()
    pipeline = args.pipeline
    genome = args.genome
    threads = args.threads
    
    remove_human(pipeline, genome, threads)

if __name__=='__main__':
    parse_args()