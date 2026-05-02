#!/bin/bash

# Directory locations
assembly_loc="../../../Methods_Comparison_Data/assembled/assembly"
db="../../../../ryan/genomad_db/genomad_db"
output_dir="genomad_commands"

# Create the output directory if it doesn't exist
mkdir -p $output_dir

# Loop over each folder in the assembly_loc directory
for folder in $assembly_loc/*; do
  if [ -d "$folder" ]; then
    folder_name=$(basename "$folder")
    output_folder="$assembly_loc/$folder_name/genomad"
    
    # Check if the output ct3 folder already exists
    if [ ! -d "$output_folder" ]; then
      # Create the Slurm job file
      job_file="$output_dir/$folder_name.slurm"
      cat <<EOL > $job_file
#!/bin/bash
#SBATCH --job-name=$folder_name
#SBATCH --output=$output_dir/$folder_name.out
#SBATCH --error=$output_dir/$folder_name.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=32G

genomad end-to-end $assembly_loc/$folder_name/${folder_name}.contigs.fa $output_folder $db --threads 10
EOL

      # Submit the job
      sbatch $job_file
    else
      echo "Output folder $output_folder already exists, skipping job submission for $folder_name."
    fi
  fi
done
