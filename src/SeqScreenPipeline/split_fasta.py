""" split_fasta.py (assumes you have biopython installed, e.g. with pip install biopython)
"""
import sys, math
import argparse
from Bio import SeqIO
import os
import glob
import subprocess



def batch_iterator(iterator, batch_size):
    """
    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    (derived from https://biopython.org/wiki/Split_large_file)
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.__next__()
            except StopIteration:
                entry = None
            if entry is None:
                break # EOF = end of file
            batch.append(entry)
        if batch:
            yield batch

def split_files(ffile: str, chunks:int, out_dir:str):
    """Splits files into n chunks

    Args:
        ffile (str): fasta file to split
        chunks (int): number of chunks to split file into
    """
    nseq = len([1 for line in open(ffile) if line.startswith(">")])
    chunksize=math.ceil(nseq/int(chunks))
    print("Splitting fasta file of", nseq, "sequences into chunks of size", chunksize)

    records = SeqIO.parse(open(ffile), "fasta")
    for i, batch in enumerate(batch_iterator(records, chunksize)):
        output_name = ffile.split('/')[-1].split(".fasta")[0]
        filename = f"{output_name}_{i+1}.fasta"
        out_loc = os.path.join(out_dir, filename)
        if not os.path.exists(out_loc):
            with open(filename, "w") as handle:
                count = SeqIO.write(batch, handle, "fasta")
            print(f"Wrote {count} sequences to {filename}")
            
            subprocess.run(['mv', filename, out_loc], check=True)
        


def parse_args():
    """Parses inputs if used
    """
    parser = argparse.ArgumentParser(description="Splits fasta file into n equivalent chunks")
    parser.add_argument('pipeline', type=str, help="Pipeline location")
    parser.add_argument('n', type=int, help="Number of chunks to split each fasta file into")

    args = parser.parse_args()
    pipeline = args.pipeline
    n = args.n

    fasta_dir = os.path.join(pipeline, 'fasta-split')
    outdir = os.path.join(pipeline, 'fasta-split/fasta-split-slow')

    # files_r1 = glob.glob(f'{fasta_dir}/*1.fasta')
    # files_r2 = glob.glob(f'{fasta_dir}/*2.fasta')
    # files = set(files_r1 + files_r2)
    
    files = glob.glob(f'{fasta_dir}/*.fasta')
    
    to_split = ['2305_P71-69764_stool_virome_CACTI_Microbiome12_R2_8.fasta',
                '2306_Pntc-00003_stool_virome_CACTI_Microbiome15_R1_1.fasta',
                '2306_Pntc-00003_stool_virome_CACTI_Microbiome15_R1_5.fasta',
                '2309_P153-01219_stool_virome_CACTI_Microbiome26_R2_4.fasta',
                '2309_P164-01251_stool_virome_CACTI_Microbiome28_R2_2.fasta']
    files = [file for file in files if file.split('/')[-1] in to_split]
    print(files)
    
    for file in files:
        output_name = file.split("/")[-1].split('.fasta')[0]
        filename = f"{output_name}_1.fasta"
        out_loc = os.path.join(outdir, filename)
        if not os.path.exists(out_loc):
            print(out_loc)
            split_files(file, n, outdir)
            
    # single_end_files = set(glob.glob(f'{fasta_dir}/*.fasta')) - files    
    # for file in single_end_files:
    #     output_name = file.split("/")[-1].split('.fasta')[0]
    #     filename = f"{output_name}_1.fasta"
    #     out_loc = os.path.join(outdir, filename)
    #     if not os.path.exists(out_loc):
    #         print(out_loc)
    #         split_files(file, n, outdir)
    
if __name__=='__main__':
    parse_args()