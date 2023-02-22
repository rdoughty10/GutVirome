"""
Runs SeqScreen on Fasta file using slurm cluster
"""
import argparse
import  os
import seqscreen_slurm


def run_seqscreen(pipeline:str, database:str, threads:int=1, sensitive:bool=True):
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

    ### need to think about how to do this, because creating a job for 150 samples
    # or more might be a bit selfish. For 8 it is probably fine tho
    for file in fasta_files:
        file_loc = os.path.join(fasta_dir, file)
        working_loc = os.path.join(seqscreen_dir, file)
        if not os.path.exists(working_loc):
            seqscreen_slurm.seqscreen(file_loc, database, working_loc, sensitive, threads=threads)


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

    args = parser.parse_args()
    pipeline = args.pipeline
    database = args.db
    threads = args.threads
    sensitive = args.sensitive

    run_seqscreen(pipeline, database, threads, sensitive)


if __name__=="__main__":
    parse_args()
