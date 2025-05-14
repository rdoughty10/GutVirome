"""Combines paired end reads into singular file
"""
import argparse
import os
import pandas as pd
import subprocess
import glob


def run_lca(pipeline:str, database:str):
    """Combines paired reads into singular file by taking lca 

    Args:
        pipeline (str): pipeline file locations
        database (str): database for taxonkit
        sensitive (bool): process sensitive output instead 
        split_files (bool): processes merged split files instead
    """
        
        
    lca_dir = os.path.join(pipeline, 'taxonkit', 'fast', 'lca_tmp')
    combined_dir = os.path.join(pipeline, 'taxonkit', 'fast', 'combined')
    
    reports = glob.glob(f'{lca_dir}/*R1.tsv')
        
    for i, r1 in enumerate(reports): ## paired end reads
        print(f'[{i+1}] {r1}')
        
        filename = r1.split('/')[-1].split('_R1.tsv')[0]
        r2 = os.path.join(lca_dir, f'{filename}_R2.tsv')
        
        if os.path.exists(r2):  ### if paired end-read exists, combine using LCA
            
            tmp_out = os.path.join(combined_dir, f'{filename}_tmp.tsv') ## file for temporary combined tsv file containing taxa from both reads
            
            if not os.path.exists(tmp_out):
                r1_df = pd.read_csv(r1, delimiter='\t', index_col=0)
                r2_df = pd.read_csv(r2, delimiter='\t', index_col=0)
                
                ## select only the read id (query) and taxonomy, merge them together, combine the two taxids into new column
                r1_df = r1_df.iloc[:,[1,-1]]
                r2_df = r2_df.iloc[:,[1,-1]]
                
                merged = pd.merge(r1_df, r2_df, on='query', how='outer')
                merged['combined_taxids'] = merged['final_taxid_x'].astype(str) + ',' + merged['final_taxid_y'].astype(str)

                ## write to a tmp tsv file to be used by taxonkit
                merged.to_csv(tmp_out, sep='\t')

            
            ## run taxonkit on tmp file (if not alreaady done)
            taxonkit_out = os.path.join(combined_dir, f'{filename}_taxonkit.tsv')
            if not os.path.exists(taxonkit_out):
                subprocess.run([
                    'taxonkit', 'lca',
                    tmp_out,
                    '-i', '5',
                    '--data-dir', database,
                    '-o', taxonkit_out,
                    '-s', ','
                ], check=True, stdout=subprocess.DEVNULL)
            
            ## read and combine two into final file with just read and final taxid
            final_out = os.path.join(combined_dir, f'{filename}.tsv')
            if not os.path.exists(final_out):
                full_df = pd.read_csv(tmp_out, delimiter='\t', index_col=0)
                lca_df = pd.read_csv(taxonkit_out, delimiter='\t', header=None, index_col=0, names=['query', 'taxid1','taxid2','combined','lca'])
            
                final = pd.merge(full_df, lca_df, how='left', on='query')[['query', 'lca']]
                final['lca'] = final['lca'].astype(str).str.replace('\.0$', '', regex=True)
                final['lca'].replace(['nan', 'NaN', 'None', '', ' '], '-', inplace=True)
                
                final.to_csv(final_out, sep='\t')
                

    ## Process the single-end reads, just need to get them into same form since no combination needed
    paired_reports = set(list(glob.glob(f'{lca_dir}/*R1.tsv')) + list(glob.glob(f'{lca_dir}/*R2.tsv')))
    single_end_reports = set(list(glob.glob(f'{lca_dir}/*.tsv'))) - paired_reports
    
    print('Processing single-end reads')
    for i, report in enumerate(single_end_reports): ## just need to get format into same as combined form
        
        print(f'[{i}] {report}')
        filename = report.split('/')[-1]
        final_out = os.path.join(combined_dir, filename)
        
        if not os.path.exists(final_out):
            df = pd.read_csv(report, delimiter='\t', index_col=0)
            df = df.iloc[:,[1,-1]]
            df = df.rename(columns={'query':'query', 'final_taxid':'lca'})
            df['lca'] = df['lca'].astype(str).str.replace('\.0$', '', regex=True)
            df['lca'].replace(['nan', 'NaN', 'None', '', ' '], '-', inplace=True)

            df.to_csv(final_out, sep='\t')

def parse_args():
    """Parses args for script
    """
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta files")
    parser.add_argument('pipeline', type=str, help="location of pipeline files")
    parser.add_argument('db', type=str, help="Taxonkit Database Location")


    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db

    run_lca(pipeline, database)


if __name__=="__main__":
    parse_args()