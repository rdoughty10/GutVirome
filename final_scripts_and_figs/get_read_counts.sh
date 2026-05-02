#!/bin/bash

# Usage: ./count_reads.sh samples.txt output.tsv
SAMPLES_FILE="samples.txt"
OUTPUT_FILE="sample_read_counts.tsv"

# Clear output file
echo -e "Sample\tReadCount" > "$OUTPUT_FILE"

while read -r SAMPLE; do
    BAM="01_bam/${SAMPLE}.sorted.bam"

    if [[ ! -f "$BAM" ]]; then
        echo "Warning: BAM file not found for $SAMPLE, skipping..."
        continue
    fi

    if [[ "$SAMPLE" == *TruSeq* ]]; then
        # Single-end
        COUNT=$(samtools view -c -F 256 "$BAM")
    else
        # Paired-end
        COUNT=$(samtools view -c -f 1 -F 64 -F 256 "$BAM")
    fi

    echo -e "${SAMPLE}\t${COUNT}" >> "$OUTPUT_FILE"
done < "$SAMPLES_FILE"

