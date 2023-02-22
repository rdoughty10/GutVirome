"""Runs any command on slurm cluster and provides options for configuring slurm job
"""

import argparse
import os


def mkdir_p(directory:str):
    '''make directory if does not exist'''
    if not os.path.exists(directory):
        os.mkdir(directory)


def slurm_job(
           command:str,
           name: str,
           days:int=1,
           hours:int=0,
           memory:int=300,
           email:str='rdd57@case.edu'):
    """Run command on slurm cluster

    Args:
        command (str, required): command to run on slurm
        name (str, required): name of job
        days (int, optional): number of days for slurm. Defaults to 1.
        hours (int, optional): number of hours for slurm. Defaults to 0.
        memory (int, optional): memory in GB for slurm. Defaults to 128.
        email (str, optional): email for slurm. Defaults to author's email. 
    """
    job_directory = f'{os.getcwd()}/.job'
    mkdir_p(job_directory)

    job_file = os.path.join(job_directory, f"{name}.slurm")


    with open(job_file, "w") as slurm:
        slurm.writelines("#!/bin/bash\n")
        if days > 0:
            slurm.writelines(f"#SBATCH -t {days}-{hours}:00:00\n")
        else:
            slurm.writelines(f"#SBATCH -t {hours}:00:00\n")
        slurm.writelines(f"#SBATCH --mem {memory}G\n")
        slurm.writelines("#SBATCH --mail-type=begin\n")
        slurm.writelines("#SBATCH --mail-type=end\n")
        slurm.writelines("#SBATCH --mail-type=fail\n")
        slurm.writelines(f"#SBATCH --mail-user={email}\n")
        slurm.writelines(f"#SBATCH --job-name={name}\n")
        slurm.writelines(command)

    os.system(f"sbatch {job_file}")


def parse_args():
    """Parses args for script"""
    parser = argparse.ArgumentParser(description="Runs SeqScreen on fasta file on slurm")
    parser.add_argument('command', type=str, help="command to run on slurm")
    parser.add_argument('name', type=str, help='name of job')
    parser.add_argument('--days', default=0, type=int,
                        help='Number of days running for slurm')
    parser.add_argument('--hours', default=12, type=int,
                        help='Number of hours running for slurm')
    parser.add_argument('--memory', default=128, type=int,
                        help='Memory for slurm (GB)')
    parser.add_argument('--email', default='rdd57@case.edu', type=str,
                        help='Email for slurm updates')

    args = parser.parse_args()
    command = args.command
    name = args.name
    days = args.days
    hours = args.hours
    memory = args.memory
    email = args.email

    slurm_job(command, name, days=days, hours=hours, memory=memory, email=email)


if __name__=="__main__":
    parse_args()
