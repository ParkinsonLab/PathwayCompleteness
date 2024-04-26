#!/bin/bash

# must run script inside DeepProZyme

# CHANGE PATH NAMES TO MATCH RELATIVE TO WHERE YOU ARE RUNNING, DEFAULT ASSUMES IMPORTED INTO $HOME, and outputs to $SCRATCH

# Define paths and options
SCRIPT_DIR="$HOME/PathwayCompleteness/"
DATA_DIR="$SCRIPT_DIR/tmp/translated_reads"
OUTPUT_DIR="$SCRATCH/deepec_outputs2"
NUM_PROCESSORS="80"
COMMAND="python $SCRIPT_DIR/DeepProZyme/run_deepectransformer.py -g cpu -b 128 -cpu $NUM_PROCESSORS"

# Loop over each line in the file
while IFS= read -r taxon_id; do
    # Define specific paths for this taxon_id
    DATA="$DATA_DIR/taxon_${taxon_id}_translated.fasta"
    OUTPUT="$OUTPUT_DIR/deepEC_${taxon_id}"
    
    # Execute the command with specific pathsa
    # echo "running command: $COMMAND -i $DATA -o $OUTPUT"
    $COMMAND -i "$DATA" -o "$OUTPUT"
done < "$SCRIPT_DIR/tmp/taxon_ids.txt"
