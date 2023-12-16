
# Genome ANI Calculator

## Overview

The Genome ANI Calculator is a Python script that calculates the Average Nucleotide Identity (ANI) based on genomes of a pair of prokaryotes. It utilizes BLAST tools for sequence alignment.

## Features

- Splits genome sequences into segments (1,020 bp) for analysis
- Creates and uses BLAST databases for efficient comparisons
- Calculates ANI for pairwise genome comparisons
- Generates an ANI tables as a result

## Requirements

- Python 3.x
- BioPython library
- BLAST tools (makeblastdb, blastn)

'Preprocessing Steps"
1. First, keep all genomes in one directory.
2. If file names contain spaces, run remove_spaces.py to replace spaces with underscores (_) in file names.
3. Then run the command as given below.

## Usage

```bash
python ANI_calculator.py --genomes-dir <path/to/genomes> --output-dir <output/directory> --formatdb-executable <path/to/makeblastdb> --blastall-executable <path/to/blastn> --num_threads <number_of_threads> --clean

Options:
--genomes-dir: Directory containing genome sequences in FASTA format.
--output-dir: Output directory for the results.
--formatdb-executable: Path to the makeblastdb executable.
--blastall-executable: Path to the blastn executable.
--num_threads: Specify the number of threads used by BLAST (default is 3).
--clean: Remove redundant files created during the analysis.


"To Generate Diagonal Heatmap with dendrogram : Run the provided script for creating a diagonal heatmap in given below link."
https://github.com/MdUmar-tech/Diagonal_Heatmap_dendrogram
