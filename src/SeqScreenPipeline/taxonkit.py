"""Runs taxonkit on outputs from seqscreen
"""
import argparse
import os
import glob
import subprocess

def run_taxonkit(pipeline:str, database:str, sensitive:bool):
    """Runs taxonkit on all pipeline files

    Args:
        pipeline (str): pipeline file locations
        database (str): database for taxonkit
        sensitive (bool): process sensitive output instead 
    """

    if sensitive:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'sensitive')
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'sensitive')
    else:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'fast')

    seqscreen_folders = glob.glob(f'{seqscreen_dir}/*.fasta')

    for output_folder in seqscreen_folders:
        report_loc = os.path.join(output_folder, 'report_generation')
        report = glob.glob(f'{report_loc}/*.tsv')
        if len(report) == 0:
            print(f'No output file available for {output_folder}')
        else:
            report = report[0]

        out_name = report.split('_seqscreen_report.tsv')[0].split("/")[-1] + ".tsv"
        output = os.path.join(taxonkit_dir, out_name)
        
        if not os.path.exists(output):
            print('taxonkit lineage',
                report,
                '-i', 2,
                '--data-dir', database,
                '-o', output,
                '-R')

            subprocess.run([
                'taxonkit', 'lineage',
                report,
                '-i', '2',
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

    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    sensitive = args.sensitive

    run_taxonkit(pipeline, database, sensitive)


if __name__=="__main__":
    parse_args()