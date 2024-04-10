#!/bin/bash
conda activate deepectransformer
# load CCEnv to run kraken2
module load CCEnv

# to access debug node
debugjob --clean 1

# path locations for necessary directories
K2_DATABASE="/project/j/jparkin/Lab_Databases/kraken2"
OUTPUT_DIR="/scratch/j/jparkin/wongkoji/outputs/kraken2"
MERGED="/scratch/j/jparkin/wongkoji/outputs/pm_merged_fq/pm_merged.fq"

# command to run kraken2 classification
kraken2 --db "/project/j/jparkin/Lab_Databases/kraken2" --report $OUTPUT_DIR/pm_mtx.kreport2 $MERGED > $OUTPUT_DIR/pm_mtx_kraken.out