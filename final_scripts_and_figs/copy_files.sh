#!/bin/bash

# Paths
input_dir="/mnt/lustre/hsm/nlsas/notape/home/uvi/be/posadalab/loretta/Methods_Comparison_Data/removed-human"
output_dir="removed-human-copy"
prefix_file="samples.txt"

# Make sure output directory exists
mkdir -p "$output_dir"

# Loop over each prefix
while IFS= read -r prefix; do
    # Copy all matching fastq files
    cp "$input_dir/${prefix}"*.fastq "$output_dir/"
done < "$prefix_file"
