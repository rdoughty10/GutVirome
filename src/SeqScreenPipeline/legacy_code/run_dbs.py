"""For group of files, finds the unmapped reads from SeqScreen and then blasts them against a set of virome databases and produces results
"""
import argparse
import os
import sys
import glob
import pandas as pd
from slurm import slurm
from src.util.blastn import blastn


def run_dbs(pipeline:str, mgv:str=None, gpd:str=None, sensitive:bool=False):
    """Generates new fasta file of non-assigned reads and runs them against given databases

    Args:
        pipeline (str): Location of pipeline files
        mgv (str, optional): Metagenomic Gut Virome database fasta file. Defaults to None.
        gpd (str, optional): Gut Phage Database database. Defaults to None.
        sensitive (bool, optional): Do it on sensitive mode. Defaults to False.
    """
    
    if sensitive:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'sensitive')
        unmapped_dir = os.path.join(pipeline, 'unmapped', 'sensitive')
    else: 
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')
        unmapped_dir = os.path.join(pipeline, 'unmapped', 'fast')
        
    fasta_dir = os.path.join(pipeline, 'fasta')

    seqscreen_folders = glob.glob(f'{seqscreen_dir}/*.output')
    
    for output_folder in seqscreen_folders:
        report_loc = os.path.join(output_folder, 'report_generation')
        report = glob.glob(f'{report_loc}/*.tsv')
        if len(report) == 0:
            print(f'No output file available for {output_folder}')
        else:
            report = report[0]

        ## get unmapped reads into a file
        read_info = pd.read_csv(report, delimiter='\t')
        no_assignment = read_info[read_info['taxid'] == '-']
        unmapped_reads = list(no_assignment['query'])
        lst_out_name = report.split('_seqscreen_report.tsv')[0].split("/")[-1] + ".lst"
        lst_output = os.path.join(unmapped_dir, lst_out_name)
        
        if not os.path.exists(lst_output):

            with open(lst_output, 'w') as out:
                for item in unmapped_reads:
                    out.write(f'{item}\n')


        ## create a new fasta file with only the unmapped reads
        out_name = report.split('_seqscreen_report.tsv')[0].split("/")[-1] + ".fasta"
        original_fasta = os.path.join(fasta_dir, out_name)
        new_fasta = os.path.join(unmapped_dir, out_name)

        print(  'seqtk',
                'subseq',
                original_fasta,
                lst_output,
                '>', 
                new_fasta)

        if not os.path.exists(new_fasta):
            command = f'seqtk subseq {original_fasta} {lst_output} > {new_fasta}'
            slurm(command, name=f'unmapped:{out_name}', days=0, hours=1, memory=1)


        # run blast queries for whichever databases are selected
        if mgv is not None:
            blastn(new_fasta, mgv, f'{out_name}xMGV', threads=32, days=0, hours=1, memory=150)
    
        if gpd is not None:
            blastn(new_fasta, gpd, f'{out_name}xGPD', threads=32, days=0, hours=1, memory=150)



def parse_args():
    """parses arguments for script"""
    parser = argparse.ArgumentParser(description='Blasts unmapped reads from seqscreen with other databases')
    parser.add_argument('pipeline', type=str, help='Location of pipeline')
    parser.add_argument('--mgv', type=str, help='Path for Metagenomic Gut Virome Database')
    parser.add_argument('--gpd', type=str, help='Path for Gut Phage Database')
    parser.add_argument('--sensitive', action='store_true', default=False, help="Use sensitive mode output")

    args = parser.parse_args()
    pipeline = args.pipeline
    mgv = args.mgv
    gpd = args.gpd

    run_dbs(pipeline, mgv, gpd)




if __name__=="__main__":
    parse_args()
