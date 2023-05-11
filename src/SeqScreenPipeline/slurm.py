"""Runs any command on slurm cluster and provides options for configuring slurm job
"""

import argparse
import os
import multiprocessing as mp
import subprocess
import time


def mkdir_p(directory:str):
    '''make directory if does not exist'''
    if not os.path.exists(directory):
        os.mkdir(directory)

def slurm(
           commands:list,
           name: str,
           days:int=1,
           hours:int=0,
           memory:int=300,
           tasks: int=1,
           nodes: int=1,
           tasks_per_node: int=1,
           threads_per_task:int=1,
           email:str='rdd57@case.edu'):
    """Run command on slurm cluster

    Args:
        command (str, required): command to run on slurm
        name (str, required): name of job
        days (int, optional): number of days for slurm. Defaults to 1.
        hours (int, optional): number of hours for slurm. Defaults to 0.
        memory (int, optional): memory in GB for slurm. Defaults to 128.
        tasks (int, optional): number of tasks in job
        nodes (int, optional): number of nodes for job
        tasks_per_node (int, optional): number of tasks per node
        threads_per_task (int, optional): number of threads per task
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
        slurm.writelines(f"#SBATCH --ntasks={tasks}\n")
        slurm.writelines(f"#SBATCH --cpus-per-task={threads_per_task}\n")
        slurm.writelines(f"#SBATCH --nodes={nodes}\n")
        slurm.writelines(f"#SBATCH --ntasks-per-node={tasks_per_node}\n")
        #slurm.writelines("#SBATCH --mail-type=begin\n")
        #slurm.writelines("#SBATCH --mail-type=end\n")
        #slurm.writelines("#SBATCH --mail-type=fail\n")
        #slurm.writelines(f"#SBATCH --mail-user={email}\n")
        slurm.writelines(f"#SBATCH --job-name={name}\n")
        for command in commands:
            slurm.writelines(f'{command}\n')

    os.system(f"sbatch {job_file}")
    
    
    
def slurm_mp(commands:list,
             processes:int,
             name: str,
             days:int=1,
             hours:int=0,
             memory_per_process:int=1,
             threads_per_process:int=1,
             email:str='rdd57@case.edu'):
    
    job_directory = f'{os.getcwd()}/.job'
    mkdir_p(job_directory)

    job_file = os.path.join(job_directory, f"{name}.slurm")

    mem_per_cpu = int(memory_per_process/threads_per_process)  
    if mem_per_cpu < 1:
        mem_per_cpu = 1
    
    commands_str = ",".join(f"'{command}'" for command in commands)

    with open(job_file, "w") as slurm:
        slurm.writelines("#!/mnt/netapp2/Store_uni/home/uvi/be/rdo/miniconda3/envs/SeqScreenEnv/lib/python3.10\n")
        if days > 0:
            slurm.writelines(f"#SBATCH -t {days}-{hours}:00:00\n")
        else:
            slurm.writelines(f"#SBATCH -t {hours}:00:00\n")
        slurm.writelines(f"#SBATCH --ntasks={processes}\n")
        slurm.writelines(f"#SBATCH --mem-per-cpu {mem_per_cpu}G\n")
        slurm.writelines(f"#SBATCH --cpus-per-task={threads_per_process}\n")
        slurm.writelines("#SBATCH --mail-type=begin\n")
        slurm.writelines("#SBATCH --mail-type=end\n")
        slurm.writelines("#SBATCH --mail-type=fail\n")
        slurm.writelines(f"#SBATCH --mail-user={email}\n")
        slurm.writelines(f"#SBATCH --job-name={name}\n")
        # for command in commands:
        #     slurm.writelines(command)
        
        slurm.writelines("import sys\n")
        slurm.writelines("import os\n")
        slurm.writelines("import multiprocessing\n")
        slurm.writelines("sys.path.append(os.getcwd())\n")

        slurm.writelines("def process_launcher(command):\n")
        slurm.writelines("\tprint(command)\n")
        slurm.writelines(f"pool = mp.Pool({processes})\n")
        slurm.writelines(f"pool.map(process_launcher, [{commands_str}])\n")
   
    
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
    command = [args.command]
    name = args.name
    days = args.days
    hours = args.hours
    memory = args.memory
    email = args.email

    slurm(command, name, days=days, hours=hours, memory=memory, email=email)


if __name__=="__main__":
    parse_args()
