"""Runs blastn query on slurm cluster
"""

import argparse
import os


def mkdir_p(directory):
    """helper function"""
    if not os.path.exists(directory):
        os.mkdir(directory)


def blastn(query:str,
           subject:str,
           out:str,
           threads:int=1,
           days:int=0,
           hours:int=12,
           memory:int=128,
           email:str='rdd57@case.edu'):
    """Run blastn on slurm cluster

    Args:
        query (str): query sequence for blast
        subject (str): query subject for blast
        out (str): output name
        threads (int, optional): number of threads. Defaults to 1.
        days (int, optional): number of days for slurm. Defaults to 0.
        hours (int, optional): number of hours for slurm. Defaults to 12.
        memory (int, optional): memory in GB for slurm. Defaults to 128.
        email (str, optional): email for slurm. Defaults to author's email. 
    """
    job_directory = f'{os.getcwd()}/.job'
    mkdir_p(job_directory)

    job_file = os.path.join(job_directory, f"{out}.slurm")
    output_dir = "blastn.out"
    mkdir_p(output_dir)

    out_file = os.path.join(os.getcwd(), output_dir, f"{out}.tsv")

    blast_query = f'blastn -query {query} -subject {subject} -out {out_file} -num_threads {threads} -outfmt "6 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"'

    with open(job_file, "w") as slurm:
        slurm.writelines("#!/bin/bash\n")
        if days > 0:
            slurm.writelines(f"#SBATCH -t {days}-{hours}:00:00\n")
        else:
            slurm.writelines(f"#SBATCH -t {hours}:00:00\n")
        slurm.writelines(f"#SBATCH --mem {memory}G\n")
        slurm.writelines(f"#SBATCH --cpus-per-task {threads}\n")
        slurm.writelines("#SBATCH --mail-type=begin\n")
        slurm.writelines("#SBATCH --mail-type=end\n")
        slurm.writelines("#SBATCH --mail-type=fail\n")
        slurm.writelines(f"#SBATCH --mail-user={email}\n")
        slurm.writelines(f"#SBATCH --job-name={out}\n")
        slurm.writelines(blast_query)

    os.system(f"sbatch {job_file}")


def parse_args():
    """Parses args if run through command line
    """
    parser = argparse.ArgumentParser(description="Runs blastn query on slurm cluster")
    parser.add_argument('query', type=str, help='query sequence (fasta file)')
    parser.add_argument('subject', type=str,
                        help='subject database (fasta file with folder of database)')
    parser.add_argument('out', type=str, help='output file name (.tsv file)')
    parser.add_argument('--threads', default=1, type=int, help='number of threads')
    parser.add_argument('--days', default=0, type=int,
                        help='Number of days running for slurm')
    parser.add_argument('--hours', default=12, type=int,
                        help='Number of hours running for slurm')
    parser.add_argument('--memory', default=64, type=int,
                        help='Memory for slurm (GB)')
    parser.add_argument('--email', default='rdd57@case.edu', type=str,
                        help='Email for slurm updates')

    args = parser.parse_args()
    query = args.query
    subject = args.subject
    out = args.out
    threads = args.threads
    days = args.days
    hours = args.hours
    memory = args.memory
    email = args.email

    print('Running blastn')
    blastn(query, subject, out, threads=threads, days=days, hours=hours, memory=memory, email=email)


if __name__=="__main__":
    parse_args()
