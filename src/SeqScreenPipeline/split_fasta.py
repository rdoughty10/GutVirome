""" split_fasta.py (assumes you have biopython installed, e.g. with pip install biopython)
"""
import sys, math
import argparse
from Bio import SeqIO



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

def split_files(ffile: str, chunks:int):
    """Splits files into n chunks

    Args:
        ffile (str): fasta file to split
        chunks (int): number of chunks to split file into
    """
    nseq = len([1 for line in open(ffile) if line.startswith(">")])
    chunksize=math.ceil(nseq/int(chunks))
    print("Splitting multi-fasta file of", nseq, "sequences into chunks of size", chunksize)

    records = SeqIO.parse(open(ffile), "fasta")
    for i, batch in enumerate(batch_iterator(records, chunksize)):
        output_name = ffile.split(".fasta")[0]
        filename = f"{output_name}_{i+1}.fasta"
        with open(filename, "w") as handle:
            count = SeqIO.write(batch, handle, "fasta")
        print(f"Wrote {count} sequences to {filename}")


def parse_args():
    """Parses inputs if used
    """
    parser = argparse.ArgumentParser(description="Splits fasta file into n equivalent chunks")
    parser.add_argument('fasta', type=str, help="Fasta input file")
    parser.add_argument('n', type=int, help="Number of chunks to split file into")

    args = parser.parse_args()
    fasta = args.fasta
    n = args.n

    split_files(fasta, n)
    