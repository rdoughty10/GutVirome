"""
Runs SeqScreen on Fasta file using slurm cluster
"""
import argparse
import  os
import seqscreen_slurm
import multiprocessing as mp
import subprocess
import time
from datetime import datetime


def run_seqscreen(pipeline:str, database:str, threads:int=1, sensitive:bool=True, local_launch:bool=False):
    """Runs seqscreen on series of files

    Args:
        pipeline (str): directory of pipeline files
        database (str): database for seqscreen
        threads (int, optional): Number of threads. Defaults to 1.
        sensitive (bool, optional): Use seqscreen sensitive mode. Defaults to True.
    """
    fasta_dir = os.path.join(pipeline, 'fasta')
    if sensitive:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'sensitive')
    else:
        seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')

    fasta_files = os.listdir(fasta_dir)
    fasta_files = [file for file in fasta_files if '.fasta' in file] ## filter any weird nextflow files that may pop up
    
    fasta_files = [file for file in fasta_files if 'P1' in file] ## testing purposes../

    ### need to think about how to do this, because creating a job for 150 samples
    # or more might be a bit selfish. For 8 it is probably fine tho
    use_slurm = not local_launch
    if use_slurm:
        print('Launching seqscreen jobs on slurm')
        for file in fasta_files:
            file_loc = os.path.join(fasta_dir, file)
            working_loc = os.path.join(seqscreen_dir, file)
            if not os.path.exists(working_loc):
                print(f'Submitting job for {file}')
                if sensitive:
                    seqscreen_slurm.seqscreen(file_loc,
                                              database,
                                              working_loc,
                                              sensitive,
                                              threads=threads,
                                              days=3)
                else:
                    seqscreen_slurm.seqscreen(file_loc,
                                              database,
                                              working_loc,
                                              sensitive,
                                              threads=threads,
                                              days=0,
                                              hours=6)
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
                        action='store_false',
                        default=False,
                        help="Launch the seqscreen from local (still uses slurm for subprocesses)")

    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    threads = args.threads
    sensitive = args.sensitive
    launch_mode = args.local_launch

    run_seqscreen(pipeline, database, threads, sensitive, launch_mode)


if __name__=="__main__":
    parse_args()
