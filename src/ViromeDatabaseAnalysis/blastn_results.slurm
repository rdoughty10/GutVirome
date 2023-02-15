#!/bin/bash
#SBATCH -t 1-00:00:00
#SBATCH --mem 256
#SBATCH --cpus-per-task 32
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-type=fail
#SBATCH --mail-user=rdd57@case.edu
#SBATCH --job-name=blastn_results                

source ~/.bashrc 
conda activate blast

blastn -query $POSADALUSTRE/loretta/virome_dbs/test.fa -subject $POSADALUSTRE/loretta/virome_dbs/MGV_blastdb/mgv_contigs.fna -outfmt "6" -out $POSADALUSTRE/loretta/virome_dbs/test.tsv -num_threads 64