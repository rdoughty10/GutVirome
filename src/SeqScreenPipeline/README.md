# SeqScreen Pipeline
This set of files pipelines the process from raw fastq samples to a processed table of seqscreen results for batched samples. The pipeline was developed in February 2023 and supports the processing of Gut Microbiome samples for processing on a slurm cluster

## Overview of Pipeline
The pipeline consists of running 9 different python scripts, which together fully process raw fastq files into a report of read numbers from seqscreen. 

1) Initialize Pipeline (initialize_pipeline.py) 
2) FastQC (fastqc.py)
3) MultiQC (multiqc.py)
4) Seqtk (seqtk.py)
5) Komplexity (komplexity.py)
6) Fasta conversion (fasta.py)
7) SeqScreen (seqscreen.py)
8) Taxonkit (taxonkit.py)
9) Report Generation (results.py)

To create a pipeline for a batch, simply initialize the pipeline as seen in step 1, and then follow along the pipeline, providing the location of the pipeline at each step


# Before running the pipeline
If running the pipeline on CESGA (Centro de Supercomputacion de Galicia), there are a few steps that need to be taken before running the pipeline. If you are on a different computing cluster, not all steps may be necessary.  

## Environment 
I have provided a full conda environment .yml file that contains a working environment for all steps of the pipeline. This conda environment can be created, activated, and confirmed using the following steps:

```
conda env create -f environment.yml
conda activate SeqScreenEnv
conda env list
```

Although you have activated this environment, Cesga's default python is often the head 

If you are running into errors when running seqscreen, such as `No module named numpy/bitarray`, check the current python version you are launching the script from using the command `python --version`. If this does not match the python version of the conda environment seen with `conda env list`, then you are using Cesga's default python environment. To fix this issue, check your path with `echo $PATH`. If your miniconda path is at the end (after the cesga paths), it may be necessary to add the path to the Python binary for the environment (path to miniconda/envs/SeqScreenEnv/bin) to your path. You can do this by modifying the ~/.bashrc or ~/.bashprofile file with the following line: `export PATH="[path to miniconda]/miniconda3/bin:$PATH`. You will need to restart your terminal afterwards, and then test to see if your python path has changed again with `python --version`. 

## Nextflow Config File
CESGA requires a time and memory specification for all slurm jobs. Unfortunately, seqscreen does not provide that with it's default slurm jobs using --slurm. Therefore, we have to provide a nextflow config file that can provide the time and memory requirements for each subprocess run by SeqScreen. While we can estimate the time and memory requirements used by each process, the values are obviously very dependent on the number of input reads as well as the waittime on the slurm cluster. For now, we have provided a config file for both fast and sensitive mode that provides a basic starting point for each. These were both developed with files around 1 million reads in mind on with short slurm wait times. When you are running a mode, simply copy the `fast_config` or `sensitive_config` to `~/.nextflow/config`. If you are trying to run both sensitive and fast mode on files at the same time, use the sensitive mode, but note that it will be slightly slower depending on the CESGA wait times. 

Automatic config file creation is still in development, so this will be updated once that is completed. Feel free to modify the config file to fit your own requirements.


# Running the Pipeline
Please note that a single script to run each step consecutively is in development, but currently is not supported.

Besides a few exceptions where databases are neeeded, the default version of most scripts are run simply by using the following command with the location of the pipeline directory initialized in step 1.

```
python [script.py] [pipeline directory]
```

Granted that they are run in the correct order, this will process your files from beginning to end. 

## Activate the environment
If you have not already follow the steps described above to activate the conda enviroment and place the correct config file in the correct place. 

## 1) Initialize pipeline
initialize_pipeline.py provides basic functionality to create the directories for the pipeline ahead of time. Simply provide the location where you would like the pipeline files to be stored as well as what you want the name of the pipeline to be. 

For example, if you wanted to create a pipeline called `cancer_genomes` in your home directory, you would use the following command:

```
python initialize_pipeline.py ~ cancer_genomes
```

You can confirm the command worked successfully by navigating to the new folder in the location and confirming that it has 9 folders, each describing a step in the pipeline.


Full information about the command is found here:

```
usage: initialize_pipeline.py [-h] output name

Initializes SeqScreen Pipeline

positional arguments:
  output      Location where output folder should be
  name        Name of batch folder

options:
  -h, --help  show this help message and exit
```

After you have confirmed the creation of the pipeline folders, move all raw fastq files you want to run through the pipeline into the fastq folder of the new directory. Then you will be ready to complete the next steps. 

## 2) FastQC
If you are just trying to use SeqScreen, FastQC is not a necessary step. However fastqc provides quality control reports that are important for most studies. 

In order to run fastqc on the fastq files simply use the command:

```
python fastqc.py [location of pipeline]
```

For example, if you wanted to process the folder you created above, you would use the command 

```
python fastqc.py ~/cancer_genomes
```

Full description of the command is seen here:
```
usage: fastqc.py [-h] pipeline

Bulk processes folder of files with fastqc

positional arguments:
  pipeline    pipeline directory

options:
  -h, --help  show this help message and exit
```


## 3) MultiQC
MultiQC is a seconday step for quality control after fastqc. 

In order to run multiqc on the fastqc reports simply use the command:

```
python multiqc.py [location of pipeline]
```

For example, if you wanted to process the folder you created above, you would use the command 

```
python multiqc.py ~/cancer_genomes
```

Full description of the command is seen here:
```
usage: multiqc.py [-h] pipeline

Bulk processes folder of files with multiqc

positional arguments:
  pipeline    pipeline directory

options:
  -h, --help  show this help message and exit
```


## 4) Seqtk
Seqtk is the first step of quality control. 

In order to run seqtk on the fastq files simply use the command:

```
python seqtk.py [location of pipeline]
```

For example, if you wanted to process the folder you created above, you would use the command 

```
python seqtk.py ~/cancer_genomes
```

Full description of the command is seen here:
```
usage: seqtk.py [-h] pipeline

Bulk processes folder of fastq files with seqtk

positional arguments:
  pipeline    pipeline directory

options:
  -h, --help  show this help message and exit
```


## 4) Komplexity
Komplexity is the second step of quality control. 

In order to run komplexity on the seqtk output files simply use the command:

```
python komplexity.py [location of pipeline]
```

For example, if you wanted to process the folder you created above, you would use the command 

```
python seqtk.py ~/cancer_genomes
```

Full description of the command is seen here:
```
usage: seqtk.py [-h] pipeline

Bulk processes folder of fastq files with seqtk

positional arguments:
  pipeline    pipeline directory

options:
  -h, --help  show this help message and exit
```

