"""
converts fastq files to fasta files with seqtk 
"""
import argparse
import os
import glob
import slurm


def fasta(pipeline:str):
    """Runs seqtk on the files to convert to fasta

    Args:
        pipeline (str): _description_
    """
    komplexity_dir = os.path.join(pipeline, 'komplexity')
    fasta_dir = os.path.join(pipeline, 'fasta')

    all_files = glob.glob(f'{komplexity_dir}/*.fastq')
    masked_files = glob.glob(f'{komplexity_dir}/*masked.fastq')
    input_files = [file.split('/')[-1] for file in all_files if file not in masked_files]

    ## process with seqtk
    for file in input_files:
        file_loc = os.path.join(komplexity_dir, file)
        fasta_name = file[:-1] + 'a'
        out_loc = os.path.join(fasta_dir, fasta_name)
        if not os.path.exists(out_loc):
            command = f'seqtk seq -A {file_loc} > {out_loc}'
            name = pipeline.split('/')[-1]
            slurm.slurm_job(command, f'{name}_fasta', hours=1, days=0, memory=16)



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
