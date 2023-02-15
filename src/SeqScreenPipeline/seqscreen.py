"""
Runs SeqScreen on Fasta file using slurm cluster
"""
import argparse
import glob, os
import multiprocessing as mp
import subprocess

def run_seqscreen(fasta:str, database:str, working:str, from_list:str=None, sensitive:bool=True, threads:int=1):
    """Runs seqscreen on series of files

    Args:
        fasta (str): directory of fasta files
        database (str): database for seqscreen
        working (str): working directory (where output goes)
        from_list (str, optional): list of fasta files to use in directory. Defaults to None.
        sensitive (bool, optional): Use seqscreen sensitive mode. Defaults to True.
        threads (int, optional): Number of threads. Defaults to 1.
    """
    fasta_files = []
    if from_list is not None:
        f = open(from_list, 'r')
        lines = f.readlines()
        fasta_files = [os.path.join(fasta, fasta_file) for fasta_file in lines]
        f.close()
    else:
        fasta_files = list(glob.glob(f'{fasta}/*.fastq'))

    pool = mp.Pool(len(fasta_files))
    pool.starmap(seqscreen_slurm, [(fasta_file, database, working, threads, sensitive)
                                   for fasta_file in fasta_files])


def seqscreen_slurm(fasta: str, database: str, working: str, threads:int=1, sensitive:bool=True):
    """Runs seqscreen sensitive mode on slurm cluster

    Args:
        fasta (str): fasta file location
        database (str): seqscreen database location
        working (str): working directory for output
        threads (int): number of threads to use (ideally 32-48)
        sensitive (bool): use sensitive mode
    """
    ## SENSITIVE 
    ## seqscreen
    # --fasta [fasta]
    # --databases [database]
    # --working [output]
    # --sensitive
    # --threads 30
    # --slurm
    
    if sensitive:
        subprocess.run([
            "seqscreen",
            "--fasta", fasta,
            "--database", database,
            "--working", working,
            "--blastn"
            "--report_prefix",
            "--report_only",
            "--sensitive",
            "--slurm",
            "--threads", threads
            ], check=True)
    elif not sensitive:
        subprocess.run([
            "seqscreen",
            "--fasta", fasta,
            "--database", database,
            "--working", working,
            "--report_prefix",
            "--report_only",
            "--slurm",
            "--threads", threads
            ], check=True)


def parse_args():
    """Parses args for script
    """
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta file")
    parser.add_argument('fasta', type=str, help="location of fasta file or directory if using -from-list")
    parser.add_argument('db', type=str, help="Seqscreen Database Location")
    parser.add_argument('working', type=str, help="Working directory")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    parser.add_argument('-from-list',
                        type=str,
                        default=None,
                        help="txt file with list of fasta files in directory to run")
    parser.add_argument('-s', '--sensitive',
                        action='store_true',
                        default=False,
                        help='Run SeqScreen in sensitive mode')

    args = parser.parse_args()
    fasta = args.fasta
    fasta_list = args.from_list
    sensitive = args.sensitive

    run_seqscreen(fasta, fasta_list, sensitive)


if __name__=="__main__":
    parse_args()
