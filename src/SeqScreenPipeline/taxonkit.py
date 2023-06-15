"""Runs taxonkit on outputs from seqscreen
"""
import argparse
import os
import glob
import subprocess

def run_taxonkit(pipeline:str, database:str, sensitive:bool, split_files:bool=False):
    """Runs taxonkit on all pipeline files

    Args:
        pipeline (str): pipeline file locations
        database (str): database for taxonkit
        sensitive (bool): process sensitive output instead 
        split_files (bool): processes merged split files instead
    """

    if sensitive:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'sensitive')
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'sensitive')
    else:
        if split_files:
            seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'final')
            reports = glob.glob(f'{seqscreen_dir}/*.tsv')
        else:
            seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')
            reports = glob.glob(f'{seqscreen_dir}/*/report_generation/*_seqscreen_report.tsv')
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'fast')
    
    for i, report in enumerate(reports):
        out_name = report.split("/")[-1]
        output = os.path.join(taxonkit_dir, out_name)
        
        if not os.path.exists(output):
            print(f'[{i+1}] {report}')
            subprocess.run([
                'taxonkit', 'lineage',
                report,
                '-i', '3',
                '--data-dir', database,
                '-o', output,
                '-R'
            ], check=True)



def parse_args():
    """Parses args for script
    """
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta files")
    parser.add_argument('pipeline', type=str, help="location of pipeline files")
    parser.add_argument('db', type=str, help="Taxonkit Database Location")
    parser.add_argument('-s', '--sensitive',
                        action='store_true',
                        default=False,
                        help='Process sensitive mode files')
    parser.add_argument('--split-files',
                        action='store_true',
                        default=False,
                        help='If files were split and then merged again')

    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    sensitive = args.sensitive
    split = args.split_files

    run_taxonkit(pipeline, database, sensitive, split)


if __name__=="__main__":
    parse_args()
    
## database for taxonkit is ../../../taxonkit_data