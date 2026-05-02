#!/bin/bash

# --- Configuration ---
INDEX_BASE="/home/uvi/be/rdo/species_index"
FASTQ_DIR="removed-human-copy"
SAMPLE_LIST="samples.txt"
OUTPUT_DIR="."
COMBINED_STATS_FILE="$OUTPUT_DIR/summary_combined_stats.tsv"

# Create directories
mkdir -p "$OUTPUT_DIR/01_bam" "$OUTPUT_DIR/02_stats" "logs"

# Initialize header for combined stats (Overwrites existing file)
echo -e "Sample_ID\tReference_Sequence\tLength\tMapped_Reads\tUnmapped_Reads" > "$COMBINED_STATS_FILE"

# Submit jobs
while IFS= read -r SAMPLE_ID || [ -n "$SAMPLE_ID" ]; do
    # Remove any Windows carriage returns and skip empty lines
    ID=$(echo "$SAMPLE_ID" | tr -d '\r')
    [[ -z "$ID" ]] && continue
    
    echo "Submitting: $ID"
    
    sbatch map_worker.slurm \
           "$ID" \
           "$INDEX_BASE" \
           "$FASTQ_DIR" \
           "$OUTPUT_DIR" \
           "$COMBINED_STATS_FILE"

done < "$SAMPLE_LIST"



