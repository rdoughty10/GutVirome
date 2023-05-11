"""
Parses blastn results between and against the two virome databases
and provides results in a more legible format
"""
import argparse
import pandas as pd
import numpy as np
import os
from io import StringIO
import pandas as pd

def parse_blastn(blastn:str, mgv:str="metadata/mgv_contig_info.tsv", gpd:str="metadata/GPD_metadata.tsv", alignment_cutoff:int=50):
    print('Reading in files:')
    blast_results = pd.read_csv(blastn, delimiter='\t', header=None)
    gpd_lookup = pd.read_csv("$POSADALUSTRE/loretta/GutVirome/src/ViromeDatabaseAnalysis/metadata/GPD_metadata.tsv", delimiter='\t')
    mgv_lookup = pd.read_csv("$POSADALUSTRE/loretta/GutVirome/src/ViromeDatabaseAnalysis/metadata/mgv_contig_info.tsv", delimiter='\t')
    print('Done')

    print('Query | MGV Contig: Genus ||| Alignment Percent    Length     Evalue')
    filtered_data = []
    for _, hit in blast_results.iterrows():
        percent_match = np.round(hit[2], 2)
        alignment_length = hit[3]
        evalue = hit[10]
        mgv_contig = mgv_lookup.loc[mgv_lookup['contig_id'] == hit[1]]
        if list(mgv_contig['completeness'])[0] > 95 and int(percent_match) > alignment_cutoff:
            family = list(mgv_contig['ictv_family'])[0]
            filtered_data.append([hit[0], hit[1], family, percent_match, alignment_length, evalue])
            #print(f'{hit[0]} | {hit[1]}:{family} ||| {percent_match}%\t{alignment_length}nt\t{evalue}')
    output_df = pd.DataFrame(filtered_data, columns=['QueryName', 'HitName', 'Family', 'PercentMatch', 'AlignmentLength', 'Evalue'])
    output_df.to_csv(f'blast_filtered_outputs/{blastn.split("/")[-1].split(".")[0]}_{alignment_cutoff}.csv')
        
    return 0

def parse_args():
    """Parses arguments from command line
    """
    parser = argparse.ArgumentParser(description="blastn parsing")
    parser.add_argument('blastn', type=str, help="blastn results file")
    parser.add_argument('-mgv', type=str,
                        help='mgv metadata file (if different than one in /metadata)')
    parser.add_argument('-gpd', type=str,
                        help="gpd metadata file (if different than one in /metadata)")
    parser.add_argument('-alignment', type=int, help='alignment identity cutoff')

    args = parser.parse_args()
    blastn = args.blastn
    mgv = args.mgv
    gpd = args.gpd
    if args.alignment is not None:
        alignment_cutoff = args.alignment
    else:
        alignment_cutoff = 50
   
    if os.path.exists(blastn):
        parse_blastn(blastn, mgv=mgv, gpd=gpd, alignment_cutoff=alignment_cutoff)



if __name__=="__main__":
    parse_args()



# time blastn -query test.fa -subject MGV_blastdb/mgv_contigs.fna -outfmt "6" -out test.tsv -num_threads 32

#seqscreen --fasta fasta/P1-2635-I-virome_S7_L001_R1_001.seqtk.mask.filter.fasta --database SeqScreenDB_21.4 --working sensitive_mode/P1-2635-I-virome_S7_L001_R1_001/ --slurm --sensitive --threads 32 --report_prefix --report_only --blastn