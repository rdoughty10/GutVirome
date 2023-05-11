import os 

count_total = 0
count_tax = 0
success = []

dir1 = '../../../AECC_patients_pipeline/seqscreen/fast'
dir2 = '../../../AECC_patients_pipeline/seqscreen/fast-failed'
dir3 = '../../../AECC_patients_pipeline/seqscreen/fast-failed2'

for dir in [dir1, dir2, dir3]:
    for folder in os.listdir(dir):
        print(folder)
        name = folder.split('.fasta')[0]
        print(name)
        if os.path.exists(os.path.join(dir, folder, 'report_generation', f'{name}_seqscreen_report.tsv')):
            print('Report Exists')
            count_tax += 1
            success.append(folder)
        else:
            print('No report')
        count_total += 1
    
print(count_tax)
print(count_total)
print(set(success))
print(len(set(success)))
        