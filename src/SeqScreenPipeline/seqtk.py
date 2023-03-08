"""
Bulk-processes files with seqtk 
"""
import argparse
import os
from src.util.slurm import slurm


def seqtk(pipeline:str):
    """Runs seqtk on the files for length and quality filtering

    Args:
        pipeline (str): _description_
    """
    fastq_dir = os.path.join(pipeline, 'fastq')
    seqtk_dir = os.path.join(pipeline, 'seqtk')

    input_files = os.listdir(fastq_dir)

    ## process with seqtk
    for file in input_files:
        file_loc = os.path.join(fastq_dir, file)
        out_loc = os.path.join(seqtk_dir, file)
        if not os.path.exists(out_loc):
            command = f'seqtk seq -q 28 -n N -L 50 {file_loc} > {out_loc}'
            name = pipeline.split('/')[-1]
            slurm(command, f'{name}_seqtk', hours=2, days=0, memory=16)



def parse_args():
    """Parses arguments for seqtk
    """
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastq files with seqtk')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing files')

    args = parser.parse_args()
    pipeline = args.pipeline

    seqtk(pipeline)

if __name__=="__main__":
    parse_args()
