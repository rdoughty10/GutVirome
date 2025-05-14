#!/bin/bash

# Directory locations
assembly_loc="../../../AECC_patients_data/assembled/assembly"
reads_loc="../../../AECC_patients_data/removed-human"
db="../../../../ryan/ct3_DBs"
output_dir="ct3_commands"

# Create the output directory if it doesn't exist
mkdir -p $output_dir

i=1

# Loop over each folder in the assembly_loc directory
for folder in $assembly_loc/*; do
  if [ -d "$folder" ]; then
    folder_name=$(basename "$folder")
    output_folder="$assembly_loc/$folder_name/ct3"
    
    # Check if the output ct3 folder already exists
    if [ ! -d "$output_folder" ]; then
      # Create the Slurm job file
      job_file="$output_dir/$folder_name.slurm"
      cat <<EOL > $job_file
#!/bin/bash
#SBATCH --job-name=$folder_name
#SBATCH --output=$output_dir/$folder_name.out
#SBATCH --error=$output_dir/$folder_name.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=32G

cenotetaker3 -c $assembly_loc/$folder_name/${folder_name}.contigs.fa -r ct3_${i} -p T -t 10 --reads $reads_loc/${folder_name}*.fastq --cenote-dbs $db
mv ct3_${i} $output_folder
EOL

      # Submit the job
      sbatch $job_file
      i=$((i + 1))
    else
      echo "Output folder $output_folder already exists, skipping job submission for $folder_name."
    fi
  fi
done
