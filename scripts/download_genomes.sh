#!/bin/bash


# CHANGE PATHS BELOW RELATIVE TO WHERE YOU ARE RUNNING FROM

# Specify the path to your text file containing accession numbers
file_path="example_data/pseudomonas_accessions.txt"

# Specify the output dir
output_directory="output/pm_zips"

# Specify the output directory for unzipped files
unzip_directory="output/pm_transcriptomes"

# Create output dir if it doesn't exist
mkdir -p "${output_directory}"

# Loop over each line in the file
while IFS= read -r accession_number; do
    # Remove any leading or trailing whitespaces
    accession_number=$(echo "${accession_number}" | tr -d '[:space:]')

    # Run the download command for each accession number
    command="datasets download genome accession ${accession_number} --include cds --filename ${output_directory}/${accession_number}.zip"
    echo "Running command: ${command}"
    ${command}
    
    # Unzip the downloaded file into the specified directory
    unzip_command="unzip -d ${unzip_directory}/${accession_number} ${output_directory}/${accession_number}.zip"
    echo "Running unzip command: ${unzip_command}"
    ${unzip_command}

done < "${file_path}"
