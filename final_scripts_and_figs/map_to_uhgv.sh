#!/bin/bash

# --- Configuration ---
INDEX_BASE="../../UHGV" # Full path and base name of your Bowtie 2 index
FASTQ_DIR="../removed-human"             # Directory containing all FASTQ files
SAMPLE_LIST="dsamples.txt"                     # Text file with one sample name per line (e.g., SampleA, SampleB)
OUTPUT_DIR="."                        # Output directory for BAM files and statistics
# ---------------------

# Check for required tools
if ! command -v bowtie2 &> /dev/null || ! command -v samtools &> /dev/null; then
    echo "Error: bowtie2 or samtools could not be found. Please ensure they are in your PATH."
    exit 1
fi

# Create output directories
mkdir -p "$OUTPUT_DIR/01_bam"
mkdir -p "$OUTPUT_DIR/02_stats"

# Check if the sample list file exists
if [ ! -f "$SAMPLE_LIST" ]; then
    echo "Error: Sample list file '$SAMPLE_LIST' not found."
    exit 1
fi

echo "--- Starting Bowtie 2 Mapping Workflow ---"
echo "Reading samples from: $SAMPLE_LIST"

# Initialize a combined summary file header
COMBINED_STATS_FILE="$OUTPUT_DIR/summary_combined_stats.tsv"
echo -e "Sample_ID\tReference_Sequence\tLength\tMapped_Reads\tUnmapped_Reads" > "$COMBINED_STATS_FILE"

# 1. Read the list of samples line by line
while IFS= read -r SAMPLE_ID; do
    # Skip empty lines
    if [ -z "$SAMPLE_ID" ]; then
        continue
    fi
    
    echo "Processing sample: $SAMPLE_ID"
    
    # Define file paths based on naming convention
    FASTQ_FILE="$FASTQ_DIR/${SAMPLE_ID}.fastq" # Adjust file extension if needed (e.g., .fq, .fastq.gz)
    BAM_OUTPUT="$OUTPUT_DIR/bams/${SAMPLE_ID}.sorted.bam"
    STATS_OUTPUT="$OUTPUT_DIR/stats/${SAMPLE_ID}.idxstats.txt"
    
    # Check if the FASTQ file exists
    if [ ! -f "$FASTQ_FILE" ]; then
        echo "Warning: FASTQ file '$FASTQ_FILE' not found. Skipping sample."
        continue
    fi

    # --- Step A: Alignment, Sorting, and Indexing ---
    echo "  > Aligning and generating sorted BAM..."
    
    # Run bowtie2, pipe SAM output to samtools view (to convert to BAM), 
    # then pipe to samtools sort, and save the final sorted BAM.
    # We use 4 threads (-p 4) as a starting point, adjust as needed.
    
    bowtie2 -x "$INDEX_BASE" \
            -U "$FASTQ_FILE" \
            -p 32 \
            --very-sensitive-local 2> "$OUTPUT_DIR/bams/${SAMPLE_ID}.log" | \
    samtools view -bS - | \
    samtools sort -o "$BAM_OUTPUT" -
    
    # Check if BAM creation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Alignment or BAM creation failed for $SAMPLE_ID. Check log file."
        continue
    fi
    
    # Index the sorted BAM file (required for idxstats)
    samtools index "$BAM_OUTPUT"
    
    # --- Step B: Get Per-Genome Mapping Statistics ---
    echo "  > Getting per-genome statistics with samtools idxstats..."
    
    # samtools idxstats outputs statistics for every reference sequence in the index.
    # Format: Reference_Sequence_Name \t Length \t Mapped_Reads \t Unmapped_Reads
    
    samtools idxstats "$BAM_OUTPUT" > "$STATS_OUTPUT"
    
    # Append statistics to the combined summary file
    # We use 'tail -n +1' to skip the first header line from idxstats output
    # And sed to prepend the sample ID to every line
    awk -v sample="$SAMPLE_ID" 'NR > 0 {print sample "\t" $0}' "$STATS_OUTPUT" >> "$COMBINED_STATS_FILE"

done < "$SAMPLE_LIST"

echo "--- Script Finished ---"
echo "All sorted BAM files are located in: $OUTPUT_DIR/bams/"
echo "Detailed idxstats files are located in: $OUTPUT_DIR/stats/"
echo "Summary of all per-genome mapping statistics is in: $COMBINED_STATS_FILE"

# Example of how to continue processing the data
echo "Next step: You can now use the $COMBINED_STATS_FILE for further analysis in R or Python."
