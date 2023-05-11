"""
Bulk-processes files with seqtk 
"""
import argparse
import os
import glob
from slurm import slurm

def seqtk(pipeline:str, alt:str=None, alt_name:str=None):
    """Runs seqtk on the files for length and quality filtering

    Args:
        pipeline (str): location of pipeline files
        alt (str): location of fastq files if not in pipeline folder
        alt_name (str): subset name of files in alt folder 
    """
    seqtk_dir = os.path.join(pipeline, 'seqtk')
    
    if alt is None:
        fastq_dir = os.path.join(pipeline, 'fastq')
        input_files = glob.glob(f'{fastq_dir}/*.fastq')
    else:
        fastq_dir = alt
        if alt_name is None:
            input_files = glob.glob(f'{fastq_dir}/*.fastq')
        else:
            all_files = glob.glob(f'{fastq_dir}/{alt_name}')
            input_files = [file for file in all_files if '.fastq' in file]

    ## process with seqtk
    for file in input_files:
        filename = file.split('/')[-1]
        file_loc = os.path.join(fastq_dir, filename)
        out_loc = os.path.join(seqtk_dir, filename)
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
    parser.add_argument('--alt-input', type=str, default=None, help='location if fastq folders are in different location')
    parser.add_argument('--alt-name', type=str, default=None, help='general name format for alt input folder fastq files')

    args = parser.parse_args()
    pipeline = args.pipeline
    alt = args.alt_input
    name = args.alt_name
    
    seqtk(pipeline, alt, name)

if __name__=="__main__":
    parse_args()
