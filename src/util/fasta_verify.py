import os
import FastaValidator

path = '../../../AECC_patients_pipeline/fasta'
for fasta in os.listdir(path):
    print(FastaValidator.fasta_validator(os.path.join(path, fasta)))
