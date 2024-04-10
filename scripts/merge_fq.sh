#!/bin/bash

# Path to the usearch binary
USEARCH_PATH="/scratch/j/jparkin/wongkoji/software/usearch"
FQ_DIR="/scratch/j/jparkin/wongkoji/data/pm_fq_files"

# Loop over accession numbers in accessions.txt
while IFS= read -r accession; do
    forward_reads="$FQ_DIR/${accession}_sim_reads1.fq"
    reverse_reads="$FQ_DIR/${accession}_sim_reads2.fq"
    merged_output="$SCRATCH/outputs/pm_merged_fq/${accession}_merged.fq"

    # Run usearch command
    "$USEARCH_PATH" -fastq_mergepairs "$forward_reads" -reverse "$reverse_reads" -fastqout "$merged_output"

    # Optionally, you can add additional processing or analysis steps here
    # For example, you might want to perform quality filtering or other steps on the merged output.

done < "/home/j/jparkin/wongkoji/projects/pseudomonas/pseudomonas_accessions.txt"

