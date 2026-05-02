#!/bin/bash
#SBATCH --job-name=bt2_map
#SBATCH --output=logs/%j_%x.out
#SBATCH --error=logs/%j_%x.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=2:00:00

# --- Parameters ---
SAMPLE_ID=$1
INDEX_BASE=$2
FASTQ_DIR=$3
OUTPUT_DIR=$4
COMBINED_STATS_FILE=$5

# Define potential file paths
R1="$FASTQ_DIR/${SAMPLE_ID}_R1.fastq"
R2="$FASTQ_DIR/${SAMPLE_ID}_R2.fastq"
SE="$FASTQ_DIR/${SAMPLE_ID}.fastq"

BAM_OUT="$OUTPUT_DIR/01_bam/${SAMPLE_ID}.sorted.bam"
CONCORDANT_BAM="$OUTPUT_DIR/01_bam/${SAMPLE_ID}.concordant.bam"
SORTED_CONCORDANT_BAM="$OUTPUT_DIR/01_bam/${SAMPLE_ID}.concordant.sorted.bam"
STATS_OUT="$OUTPUT_DIR/02_stats/${SAMPLE_ID}.idxstats.txt"

echo "Processing sample: $SAMPLE_ID"

# --- Read Type Detection and Alignment ---
if [[ -f "$R1" && -f "$R2" ]]; then
    echo "  > Paired-end detected: $R1 and $R2"
    CMD="bowtie2 -x $INDEX_BASE -1 $R1 -2 $R2"
    FILTER_FLAGS="-f 2 -f 64 -F 256 -F 2048"
elif [[ -f "$R1" ]]; then
    echo "  > Single-end (_R1) detected: $R1"
    CMD="bowtie2 -x $INDEX_BASE -U $R1"
    FILTER_FLAGS="-F 256 -F 2048"
elif [[ -f "$SE" ]]; then
    echo "  > Single-end (.fastq) detected: $SE"
    CMD="bowtie2 -x $INDEX_BASE -U $SE"
    FILTER_FLAGS="-F 256 -F 2048"
else
    echo "Error: No FASTQ files found for $SAMPLE_ID. Checked for _R1, _R2, and .fastq"
    exit 1
fi

# Execute alignment, piping to samtools for sorting
$CMD -p "$SLURM_CPUS_PER_TASK" --very-sensitive-local 2> "$OUTPUT_DIR/01_bam/${SAMPLE_ID}.log" | \
samtools view -bS - | \
samtools sort -@ 4 -o "$BAM_OUT" -

# --- Indexing and Stats ---
# 1. Index the original BAM
samtools index "$BAM_OUT"

samtools view -b $FILTER_FLAGS "$BAM_OUT" > "$CONCORDANT_BAM"
samtools sort -o "$SORTED_CONCORDANT_BAM" "$CONCORDANT_BAM"
samtools index "$SORTED_CONCORDANT_BAM"
samtools idxstats "$SORTED_CONCORDANT_BAM" > "$STATS_OUT"

# --- Thread-safe append to summary file ---
exec 200>>"$COMBINED_STATS_FILE"
flock -x 200
# Filter out the '*' unmapped line and append
grep -v "*" "$STATS_OUT" | awk -v sample="$SAMPLE_ID" '{print sample "\t" $0}' >> "$COMBINED_STATS_FILE"
flock -u 200
