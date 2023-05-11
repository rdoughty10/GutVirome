"""
Bulk-processes files with komplexity 
"""
import argparse
import os
from slurm import slurm


def komplexity(pipeline:str):
    """Runs komplexity on the files for masking and filtering

    Args:
        pipeline (str): _description_
    """
    seqtk_dir = os.path.join(pipeline, 'seqtk')
    komplexity_dir = os.path.join(pipeline, 'komplexity')

    input_files = os.listdir(seqtk_dir)

    ## process with komplexity
    for file in input_files:
        input_file = os.path.join(seqtk_dir, file)
        file_name = file.split('.')[-0]
        output_file = os.path.join(komplexity_dir, f'{file_name}_masked.fastq')
        output_file_filtered = os.path.join(komplexity_dir, f'{file}')
        if not os.path.exists(output_file):
            command = f'kz --mask < {input_file} > {output_file}\nkz --filter < {output_file} > {output_file_filtered}'
            name = pipeline.split('/')[-1]
            slurm(command, f'{name}_komplexity', hours=2, days=0, memory=16)



def parse_args():
    """Parses arguments for komplexity 
    """
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastqc files with multiqc')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing fastq files')

    args = parser.parse_args()
    pipeline = args.pipeline

    komplexity(pipeline)

if __name__=="__main__":
    parse_args()
