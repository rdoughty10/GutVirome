"""Runs taxonkit on outputs from seqscreen
"""
import argparse
import os
import pandas as pd
import subprocess
import glob


def get_taxa(taxid, centrifuge, centrifuge_lca, diamond, diamond_lca):
    '''Helper function to do logic for determining final taxa from lca of diamond and centrifuge'''
    if taxid == '-':
        return '-'
    else:
        if centrifuge != '-':
            if ',' in centrifuge:
                return str(int(centrifuge_lca))
            else:
                return str(int(centrifuge))
        elif diamond != '-':
            if ',' in diamond:
                return str(int(diamond_lca))
            else:
                return str(int(diamond))

def run_lca(pipeline:str, database:str, sensitive:bool, split_files:bool=False):
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
        taxonkit_dir = os.path.join(pipeline, 'taxonkit', 'fast', 'lca_tmp')
        
    reports = [report for report in reports if '8659U-29-06-viromeT_S5_L001' not in report]
    reports = [report for report in reports if '5015U-29-06-viromeT_S2_L001' not in report]
    reports = [report for report in reports if '4397U-29-06-viromeT_S4_L001' not in report]
    
    for i, report in enumerate(reports):
        print(f'[{i+1}] {report}')
        out_name = os.path.join(taxonkit_dir, report.split('/')[-1])

        if not os.path.exists(out_name):
            out_name_centrifuge = report.split("/")[-1].split('.tsv')[0] + "_centrifuge.tsv"
            out_name_diamond = report.split("/")[-1].split('.tsv')[0] + "_diamond.tsv"
            
            centrifuge_output = os.path.join(taxonkit_dir, out_name_centrifuge)
            diamond_output = os.path.join(taxonkit_dir, out_name_diamond)
            
            if not os.path.exists(centrifuge_output):
                subprocess.run([
                    'taxonkit', 'lca',
                    report,
                    '-i', '4',
                    '--data-dir', database,
                    '-o', centrifuge_output,
                    '-s', ','
                ], check=True, stdout=subprocess.DEVNULL)
                
            if not os.path.exists(diamond_output):
                subprocess.run([
                    'taxonkit', 'lca',
                    report,
                    '-i', '5',
                    '--data-dir', database,
                    '-o', diamond_output,
                    '-s', ','
                ], check=True, stdout=subprocess.DEVNULL)
                
            initial_file = pd.read_csv(report, delimiter='\t')
            centrifuge_out = pd.read_csv(centrifuge_output, delimiter='\t', header=None)
            diamond_out = pd.read_csv(diamond_output, delimiter='\t', header=None)
            
            merged_df = initial_file.merge(centrifuge_out[[1,45]], left_on='query', right_on=1, how='left').merge(diamond_out[[1,45]], left_on='query', right_on=1, how='left')
            merged_df['final_taxid'] = merged_df.apply(lambda x: get_taxa(x['taxid'], x['centrifuge_multi_tax'], x['45_x'], x['diamond_multi_tax'], x['45_y']), axis=1)

            merged_df.to_csv(out_name, sep='\t')



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

    run_lca(pipeline, database, sensitive, split)


if __name__=="__main__":
    parse_args()
    
