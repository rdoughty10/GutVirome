'''Runs reference inference module seperately on the seqscreen outputs'''
import os
import argparse

from slurm import slurm

def reference_inference(pipeline=str, database=str, threads=int):
    full_fasta_files = os.path.join(pipeline, 'fastp')
    seqscreen_reports = os.path.join(pipeline, 'seqscreen', 'final')
    
    for report in os.listdir(seqscreen_reports)[:1]:
        sample_name = report.split('.tsv')[0]
        report_path = os.path.join(seqscreen_reports, report)
        fasta_path = os.path.join(full_fasta_files, f'{sample_name}.fasta')
        
        working_dir = os.path.join(pipeline, 'reference_inference', sample_name)
        
    
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)
        command = f'python seqscreen_reference_inference.py --fasta1 {fasta_path} -o {report_path} -w {working_dir} -d {database} --threads {threads} --online'
        #print(command)
        slurm([command], f'{sample_name}_ref_inf', hours=6, memory=100, days = 0, threads_per_task=threads)


def parse_args():
    parser = argparse.ArgumentParser(description='Runs reference inference on bulk seqscreen pipeline')
    parser.add_argument('pipeline', type=str, help="location of pipeline files")
    parser.add_argument('db', type=str, help="Seqscreen Database Location")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    
    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    threads = args.threads
    
    reference_inference(pipeline, database, threads)
    
    
    
if __name__=='__main__':
    parse_args()