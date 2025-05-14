#!/bin/bash

# Set the input and output directories
input_dir="../../../Methods_Comparison_Data/removed-human"
output_dir="../../../Methods_Comparison_Data/assembled/assembly"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"
mkdir -p "$output_dir/logs"

# Loop through all paired-end files (_R1.fastq)
for file_R1 in $input_dir/*R1.fastq; do
    # Generate the corresponding _R2.fastq file path
    file_R2="${file_R1/_R1.fastq/_R2.fastq}"

    # Extract the base name from the input file
    base_name=$(basename "$file_R1" _R1.fastq)

    output_subdir="${output_dir}/${base_name}"

    # Create a SLURM script for this specific paired-end file
    
    cat <<EOF > "megahit_commands/${base_name}_megahit.sh"
#!/bin/bash
#SBATCH --job-name=${base_name}_megahit
#SBATCH --time=6:00:00
#SBATCH --mem=256G
#SBATCH --cpus-per-task=20

# Run MEGAHIT assembly
megahit -1 $file_R1 -2 $file_R2 -o ${output_dir}/${base_name} --out-prefix ${base_name} -t 20 --min-contig-len 250
EOF

    
    # Submit the job to SLURM
    if [ -d "$output_subdir" ]; then
        echo "Output for ${base_name} already exists, skipping..."
        continue
    else
        echo $output_subdir
        sbatch "megahit_commands/${base_name}_megahit.sh"
    fi

done

for file_R in $input_dir/*TruSeq*.fastq; do

    base_name=$(basename "$file_R" .fastq)
    output_subdir="${output_dir}/${base_name}"

    # Create a SLURM script for this specific paired-end file
    
    cat <<EOF > "megahit_commands/${base_name}_megahit.sh"
#!/bin/bash
#SBATCH --job-name=${base_name}_megahit
#SBATCH --time=6:00:00
#SBATCH --mem=256G
#SBATCH --cpus-per-task=20

# Run MEGAHIT assembly
megahit -r $file_R -o ${output_dir}/${base_name} --out-prefix ${base_name} -t 20 --min-contig-len 250
EOF

    
    # Submit the job to SLURM
    if [ -d "$output_subdir" ]; then
        echo "Output for ${base_name} already exists, skipping..."
        continue
    else
        echo $output_subdir
        sbatch "megahit_commands/${base_name}_megahit.sh"
    fi


done