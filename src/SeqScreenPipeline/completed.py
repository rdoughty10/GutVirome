import os
import sys
from collections import defaultdict

pipeline = '../../../AECC_patients_data'

fasta_dir = os.path.join(pipeline, 'fasta-split')
seqscreen_dir = os.path.join(pipeline, 'seqscreen', 'fast')

fasta_files = sorted(os.listdir(fasta_dir))

counts = defaultdict(int)
missing = {}

splits = 10
print(len(fasta_files))

for file in fasta_files:
    file_loc = os.path.join(fasta_dir, file)
    working_loc = os.path.join(seqscreen_dir, f'{file}')
    report_generated = os.path.exists(os.path.join(working_loc, 'report_generation'))
    file_name = '_'.join(file.split('_')[:-1])
    if report_generated:
        counts[file_name] += 1
    else: 
        if file_name not in missing.keys():
            missing[file_name] = []
            file_num = file.split('_')[-1].split('.')[0]
            missing[file_name].append(file_num)
        else:
            file_num = file.split('_')[-1].split('.')[0]
            missing[file_name].append(file_num)

completed = 0
files_processed = 0
for index, value in counts.items():
    # print(f'{index}: {value}')
    if value == splits:
        completed += 1
    elif value < splits:
        print(f'Not completed: {index}  [{value}/{splits}] -- {missing[index]}')
    files_processed += value
    
    # print(f'{index}: {value}')
    
print('\n\nOverview Stats:')
print(f'Samples Fully Processed: {completed}/{int(len(fasta_files)/splits)} ({round(completed/(len(fasta_files)/splits) * 100, 2)}%)')
print(f'Files fully processed: {files_processed}/{len(fasta_files)} ({round(files_processed/(len(fasta_files)) * 100, 2)}%)\n\n')
