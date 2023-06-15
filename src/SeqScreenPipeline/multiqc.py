"""
Bulk-processes files with multiqc 
"""
import argparse
import os
from slurm import slurm



def multiqc(pipeline:str):
    """Runs fastqc on the files

    Args:
        pipeline (str): _description_
    """
    fastqc_dir_raw = os.path.join(pipeline, 'fastqc', 'raw')
    fastqc_dir_fastp = os.path.join(pipeline, 'fastqc', 'fastp')
    fastqc_dir_no_human = os.path.join(pipeline, 'fastqc', 'removed-human')
    multiqc_dir = os.path.join(pipeline, 'multiqc')


    ## process with multiqc
    command1 = f'multiqc {fastqc_dir_raw}/*fastqc.zip -o {multiqc_dir} -n raw_data'
    command2 = f'multiqc {fastqc_dir_fastp}/*fastqc.zip -o {multiqc_dir} -n fastp_data'
    command3 = f'multiqc {fastqc_dir_no_human}/*fastqc.zip -o {multiqc_dir} -n removed_human_data'
    name = pipeline.split('/')[-1]
    slurm([command1, command2, command3], f'{name}_multiqc', hours=1, days=0, memory=4)



def parse_args():
    """Parses arguments for fastqc 
    """
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastqc files with multiqc')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing files')

    args = parser.parse_args()
    pipeline = args.pipeline

    multiqc(pipeline)

if __name__=="__main__":
    parse_args()
