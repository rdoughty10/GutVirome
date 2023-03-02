"""
Bulk-processes files with multiqc 
"""
import argparse
import os
import slurm


def multiqc(pipeline:str):
    """Runs fastqc on the files

    Args:
        pipeline (str): _description_
    """
    fastqc_dir = os.path.join(pipeline, 'fastqc')
    multiqc_dir = os.path.join(pipeline, 'multiqc')

    ## process with multiqc
    command = f'multiqc {fastqc_dir}/*fastqc.zip -o {multiqc_dir}'
    name = pipeline.split('/')[-1]
    slurm.slurm_job(command, f'{name}_multiqc', hours=6, days=0, memory=16)



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
