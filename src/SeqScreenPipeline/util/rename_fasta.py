import os
import subprocess


directory = '../../../fastq/virome_fastq/AECC_patients/'

for file in os.listdir(directory):
    old = os.path.join(directory, file)
    parts = file.split('.')
    new = os.path.join(directory, f'{parts[0]}.fastq')
    
    subprocess.run([
        'mv', 
        old,
        new
    ], check=True)
    
    # print(  'mv', 
    #     old,
    #     new)
