"""Runs seqscreen query on slurm cluster
"""

import argparse
import os

def mkdir_p(directory:str):
    '''make directory if does not exist'''
    if not os.path.exists(directory):
        os.mkdir(directory)

def seqscreen(fasta:str,
           database:str,
           working:str,
           sensitive:bool=False,
           threads:int=1,
           days:int=3,
           hours:int=0,
           memory:int=10,
           email:str='rdd57@case.edu',
           no_subslurm:bool=False,
           tmp_directory:str=None):
    """Run blastn on slurm cluster

    Args:
        query (str): query sequence for blast
        subject (str): query subject for blast
        out (str): output name
        sensitive (bool): run sensitive mode. Defaults to False
        threads (int, optional): number of threads. Defaults to 1.
        days (int, optional): number of days for slurm. Defaults to 1.
        hours (int, optional): number of hours for slurm. Defaults to 0.
        memory (int, optional): memory in GB for slurm. Defaults to 128.
        email (str, optional): email for slurm. Defaults to author's email.
        subslurm (bool, option): do not use heirarchical structure.
    """
    job_directory = f'{os.getcwd()}/.job'
    mkdir_p(job_directory)

    outname = fasta.split("/")[-1]
    job_file = os.path.join(job_directory, f"{outname}.slurm")
    
    if no_subslurm:
        if sensitive:
            print('No subslurm sensitive job:')
            seqscreen_query = f'seqscreen --fasta {fasta} --databases {database} --working {working} --threads {threads} --report_prefix --sensitive --blastn --online'
            days = 3
            hours = 0
            memory = 300
        else:
            print('No subslurm fast job:')
            seqscreen_query = f'seqscreen --fasta {fasta} --databases {database} --working {working} --threads {threads} --report_prefix --online'
            days = 0
            hours = 6
            memory = 200
    else:
        if sensitive:
            seqscreen_query = f'seqscreen --fasta {fasta} --databases {database} --working {working} --slurm --threads {threads} --report_prefix --sensitive --blastn --online'
        else:
            seqscreen_query = f'seqscreen --fasta {fasta} --databases {database} --working {working} --slurm --threads {threads} --report_prefix --online'
            memory = 5
            hours = 18
            
    with open(job_file, "w") as slurm:
        slurm.writelines("#!/bin/bash\n")
        if days > 0:
            slurm.writelines(f"#SBATCH -t {days}-{hours}:00:00\n")
        else:
            slurm.writelines(f"#SBATCH -t {hours}:00:00\n")
        if not no_subslurm:
            slurm.writelines("#SBATCH -C clk\n")
        slurm.writelines(f"#SBATCH --mem {memory}G\n")
        # slurm.writelines("#SBATCH --mail-type=begin\n")
        # slurm.writelines("#SBATCH --mail-type=end\n")
        # slurm.writelines("#SBATCH --mail-type=fail\n")
        # slurm.writelines(f"#SBATCH --mail-user={email}\n")
        slurm.writelines(f"#SBATCH --job-name={outname}\n")
        if no_subslurm:
            slurm.writelines("#SBATCH --nodes=1\n")
            slurm.writelines(f"#SBATCH --cpus-per-task={threads}\n")
        # if tmp_directory is not None:
        #     slurm.writelines(f"cd {tmp_directory}")
        
        slurm.writelines("current_directory=$(pwd)\n")
        slurm.writelines('export TMPDIR="$current_directory"\n')
        slurm.writelines(seqscreen_query)

    os.system(f"sbatch {job_file}")


def parse_args():
    """Parses args for script"""
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta file on slurm")
    parser.add_argument('fasta', type=str, help="location of fasta file")
    parser.add_argument('db', type=str, help="Seqscreen Database Location")
    parser.add_argument('working', type=str, help="Working directory")
    parser.add_argument('-s', '--sensitive',
                    action='store_true',
                    default=False,
                    help='Run SeqScreen in sensitive mode')
    parser.add_argument('--threads', default=1, type=int, help='number of threads')
    parser.add_argument('--days', default=2, type=int,
                        help='Number of days running for slurm')
    parser.add_argument('--hours', default=0, type=int,
                        help='Number of hours running for slurm')
    parser.add_argument('--memory', default=1, type=int,
                        help='Memory for slurm (GB)')
    parser.add_argument('--email', default='rdd57@case.edu', type=str,
                        help='Email for slurm updates')

    args = parser.parse_args()
    fasta = args.fasta
    database = args.db
    working = args.working
    sensitive = args.sensitive
    threads = args.threads
    days = args.days
    hours = args.hours
    memory = args.memory
    email = args.email

    print('Running seqscreen')
    seqscreen(fasta, database, working, sensitive, threads=threads, days=days, hours=hours, memory=memory, email=email)


if __name__=="__main__":
    parse_args()
