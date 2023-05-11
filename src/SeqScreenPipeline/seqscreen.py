"""
Runs SeqScreen on Fasta file using slurm cluster
"""
import argparse
import  os
import multiprocessing as mp
import subprocess
import time
import shutil
from datetime import datetime
import seqscreen_slurm


def initiate_tmp_directory(current_path:str, filename: str):
    tmp_dir = os.path.join(current_path, f'tmp-{filename}')
    if os.path.exists(tmp_dir):
        subprocess.run([
            'rm', '-rf',
            tmp_dir
        ], check=True)
    os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    
        
def remove_tmp_directory(current_path:str, filename:str):
    os.chdir(current_path)
    shutil.rmtree(os.path.join(current_path, f'tmp-{filename}'))

def run_seqscreen(pipeline:str, database:str, threads:int=1, sensitive:bool=True, local_launch:bool=False, one_job:bool=False, sep_directories:bool=False, split=False):
    """Runs seqscreen on series of files

    Args:
        pipeline (str): directory of pipeline files
        database (str): database for seqscreen
        threads (int, optional): Number of threads. Defaults to 1.
        sensitive (bool, optional): Use seqscreen sensitive mode. Defaults to True.
    """
    if split:
        fasta_dir = os.path.join(pipeline, 'fasta-split')
    else:
        fasta_dir = os.path.join(pipeline, 'fasta')
        
    if sensitive:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'sensitive')
    else:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')

    fasta_files = os.listdir(fasta_dir)
    fasta_files = [file for file in fasta_files if '.fasta' in file] ## filter any weird nextflow files that may pop up
    
    #fasta_files = [file for file in fasta_files if file.split('2303_P')[-1].split('-')[0].isnumeric() and int(file.split('2303_P')[-1].split('-')[0]) >= 50] ## testing purposes../
    #fasta_files = [file for file in fasta_files if ('mock' in file and '_1' in file)]
    #fasta_files = [file for file in fasta_files if '2303_P1-32635_stool_virome_CACTI_Microbiome8_R1_3' in file]
    print(fasta_files)
    
    
    if sep_directories:
        database = '../' + database

    ### need to think about how to do this, because creating a job for 150 samples
    # or more might be a bit selfish. For 8 it is probably fine tho
    use_slurm = not local_launch
    if use_slurm:
        print('Launching seqscreen jobs on slurm')
        for file in fasta_files:
            file_loc = os.path.join(fasta_dir, file)
            working_loc = os.path.join(seqscreen_dir, f'{file}')
            report_generated = os.path.exists(os.path.join(working_loc, 'report_generation'))
            
            
            if not report_generated:
                
                if os.path.exists(working_loc):
                    subprocess.run([
                        'rm', '-r',
                        working_loc
                    ], check=True)
                
                #initiate a temp directory to launch seqscreen from -- solves nextflow problem with running multiple instances at the same time
                if sep_directories:
                    initial_working_directory = os.getcwd()
                    tmp_dir_name = f'{file}_fast' if not sensitive else f'{file}_sensitive'
                    initiate_tmp_directory(initial_working_directory, tmp_dir_name)
                    file_loc = '../' + file_loc ## ugly temp solutions
                    working_loc = '../' + working_loc
                                
                ## run seqscreen
                print(f'Submitting job for {file}')
                

                
                if sensitive:
                    seqscreen_slurm.seqscreen(file_loc,
                                              database,
                                              working_loc,
                                              sensitive,
                                              threads=threads,
                                              days=2,
                                              hours=0,
                                              no_subslurm=one_job)
                else:
                    seqscreen_slurm.seqscreen(file_loc,
                                              database,
                                              working_loc,
                                              sensitive,
                                              threads=threads,
                                              days=0,
                                              hours=6,
                                              no_subslurm=one_job)
                 
                if sep_directories:
                    os.chdir(initial_working_directory)
                    
                ## remove the tmp directory --> need to figure out a way to track the slurm calls
                ##remove_tmp_directory(initial_working_directory, file)
    else:
        data = [(os.path.join(fasta_dir, file), database, os.path.join(seqscreen_dir, file), sensitive, threads) for file in fasta_files if not os.path.exists(os.path.join(seqscreen_dir, file))]
        pool = mp.Pool(8)
        pool.starmap(seqscreen, data)


def seqscreen(fasta: str, database: str, working: str, sensitive:bool, threads:int):
    """Runs seqscreen file locally using subprocess

    Args:
        fasta (str): fasta file
        database (str): database for seqscreen
        working (str): output for seqscreen
        threads (int, optional): Number of threads
        sensitive (bool, optional): Use seqscreen sensitive mode
    """
    
    print(f'Launching seqscreen (Sensitive={sensitive}) for file: {fasta} at {datetime.now().strftime("%H:%M:%S")}')

    if sensitive:
        subprocess.run([
            'seqscreen',
            '--fasta', fasta,
            '--databases', database,
            '--working', working,
            '--slurm',
            '--threads', str(threads),
            '--report_prefix',
            '--sensitive',
            '--blastn'
        ],  check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
    else:
        subprocess.run([
            'seqscreen',
            '--fasta', fasta,
            '--databases', database,
            '--working', working,
            '--slurm',
            '--threads', str(threads),
            '--report_prefix'
        ],  check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

    print(f'Completed seqscreen (Sensitive={sensitive}) for file: {fasta} at {datetime.now().strftime("%H:%M:%S")}')


def parse_args():
    """Parses args for script
    """
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta files")
    parser.add_argument('pipeline', type=str, help="location of pipeline files")
    parser.add_argument('db', type=str, help="Seqscreen Database Location")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    parser.add_argument('-s', '--sensitive',
                        action='store_true',
                        default=False,
                        help='Run SeqScreen in sensitive mode')
    parser.add_argument('--local-launch',
                        action='store_true',
                        default=False,
                        help="Launch the seqscreen from local (still uses slurm for subprocesses)")
    parser.add_argument('--one-job',
                        action='store_true',
                        default=False,
                        help="Launch on slurm but do not use slurm inside job")
    parser.add_argument('--sep-dir',
                        action='store_true',
                        default=False,
                        help="Launch jobs in seperate directories")
    parser.add_argument('--split-input',
                        action='store_true',
                        default=False,
                        help='Run seqscreen on split fasta files rather than complete')
    

    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    threads = args.threads
    sensitive = args.sensitive
    launch_mode = args.local_launch
    one_job = args.one_job
    sep_dir = args.sep_dir

    run_seqscreen(pipeline, database, threads, sensitive, launch_mode, one_job, sep_dir)


if __name__=="__main__":
    parse_args()
