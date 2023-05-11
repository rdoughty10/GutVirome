'''Merges split files into singular output files'''
import argparse
import os
import pandas as pd
import glob

def merge_results(pipeline:str, splits:int):
    '''Takes split output folders and number of splits'''
    fasta_dir = os.path.join(pipeline, 'fasta')
    seqscreen_split_dir = os.path.join(pipeline, 'seqscreen', 'fast')
    output_dir = os.path.join(pipeline, 'seqscreen', 'final')
    
    count = 0
    
    for i, file in enumerate(os.listdir(fasta_dir)):
        basename = file.split('.fasta')[0]
        search = os.path.join(seqscreen_split_dir, basename)
        output_files = glob.glob(f'{search}*/report_generation/*_seqscreen_report.tsv')
        if len(output_files) == splits:
            outname = os.path.join(output_dir, f'{basename}.tsv')
            if not os.path.exists(outname):
                output_df = pd.DataFrame()
                count += 1
                print(f'[{count}] {file}')
                for report in output_files:
                    df = pd.read_csv(report, delimiter='\t')
                    output_df = pd.concat([output_df, df], ignore_index=True)
                output_df.to_csv(outname, sep='\t')
            


def parse_args():
    '''Parses arguments'''
    parser = argparse.ArgumentParser(
        description='Bulk processes folder of fastq files into fasta')
    parser.add_argument('pipeline', type=str, help='pipeline directory containing fastq files')
    parser.add_argument('splits', type=int, help='Number of splits if consistent')

    args = parser.parse_args()
    pipeline = args.pipeline
    splits = args.splits

    merge_results(pipeline, splits)

if __name__=="__main__":
    parse_args()
    