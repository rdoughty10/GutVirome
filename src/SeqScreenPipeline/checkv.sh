#!/bin/bash

# Directory containing your subdirectories with FASTA files
parent_dir="../../../Methods_Comparison_Data/assembled/assembly"  # Change this to the parent directory containing your subdirectories

# Loop through each subdirectory
for dir in $parent_dir/*/; do
    # Extract the base name of the directory (file_name)
    file_name=$(basename "$dir")
    
    # Define the path to the FASTA file and output directory
    fasta_file="${dir}${file_name}.contigs.fa"
    output_dir="${dir}/checkv"

    if [ -d "$output_dir" ] && [ "$(ls -A $output_dir)" ]; then
        echo "Output for $file_name already exists, skipping submission."
    else
        # Define the SLURM script content
        #Create the SLURM script
        cat <<EOF > "checkv_commands/${file_name}_checkv.sh"
#!/bin/bash
#SBATCH --job-name=${file_name}_checkv
#SBATCH --time=1:00:00
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=10

# Run CheckV
checkv end_to_end "$fasta_file" "$output_dir" -t 10 -d ../../../../ryan/VIMERA_DB_1.0/checkv-db-v1.5/
EOF

        # Submit the job to SLURM
        sbatch "checkv_commands/${file_name}_checkv.sh"
        # echo "SLURM script created and submitted for $file_name"
    fi
done
