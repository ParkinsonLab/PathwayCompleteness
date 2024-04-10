#!/bin/bash

# Path to ART illumina application
art=$HOME/software/art_bin_MountRainier/art_illumina

# Path to the folder containing the reference genomes
genome_folder=$SCRATCH/outputs/pm_transcriptomes

# Path to the folder where you want to save simulated reads
output_folder=$SCRATCH/data/pm_simulated_reads

# Path to the text file containing accession numbers, one per line
accession_file=/home/j/jparkin/wongkoji/projects/pseudomonas/pseudomonas_accessions.txt

# Loop over each accession number in the file
while IFS= read -r accession_number; do
    # Path to the reference genome
    genome_path=$(find "${genome_folder}/${accession_number}/ncbi_dataset/data/${accession_number}/" -type f -regex ".*${accession_number}.*\.fna" -print -quit)    
    # Output file name for simulated reads
    output_file="${output_folder}/${accession_number}_sim_reads"
    count=$(grep -c "^>" "$genome_path")
    echo $count
    # Run ART to simulate reads
    # $art -ss HS25 -i "${genome_path}" -p -l 150 -f 20 -m 200 -s 10 -o "${output_file}"
    divided_value=$((10000 / count + 1))
    echo "value" $divided_value
    $art -ss HS25 -i "${genome_path}" -p -l 150 -m 200 -c "$divided_value" -s 10 -o "${output_file}"

    
    echo "Simulated reads for ${accession_number} saved to ${output_file}"
done < "$accession_file"
