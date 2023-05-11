# UTIL Scripts
The util folder contains an assortment of scripts that all assist with random tasks including parsing files, generating graphs, etc. This document contains an overview of some of the scripts and primary functions of each of them.


## SLURM Scripts
Within util there are a number of scripts that automatically create and submit slurm jobs for different programs. For each, you are able to specify the time and memory requirements as well as an email adress for updates. Here is a description of what each of them does. 

### blastn.py
This script automatically runs BlastN on a query and subject. 

```
positional arguments:
  query              query sequence (fasta file)
  subject            subject database (fasta file with folder of database)
  out                output file name (.tsv file)

optional arguments:
  -h, --help         show this help message and exit
  --threads THREADS  number of threads
  --days DAYS        Number of days running for slurm
  --hours HOURS      Number of hours running for slurm
  --memory MEMORY    Memory for slurm (GB)
  --email EMAIL      Email for slurm updates
```

### seqscreen_slurm.py
This script automatically runs SeqScreen on a fasta file, either in sensitive or fast mode. 

```
positional arguments:
  fasta              location of fasta file
  db                 Seqscreen Database Location
  working            Working directory

optional arguments:
  -h, --help         show this help message and exit
  -s, --sensitive    Run SeqScreen in sensitive mode
  --threads THREADS  number of threads
  --days DAYS        Number of days running for slurm
  --hours HOURS      Number of hours running for slurm
  --memory MEMORY    Memory for slurm (GB)
  --email EMAIL      Email for slurm updates
```


Note: For SeqScreen to work with the --slurm call on the CESGA slurm cluster, you must specify a Nextflow config file in ~/.nextflow/config such as the following:

```
process {
        executor = "slurm"

        cpus='32'
        memory="300G"
        time="1d"
}
```

