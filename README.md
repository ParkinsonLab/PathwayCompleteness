## Background
Here, we perform metatranscriptomic analysis on pathway completeness per taxon to improve taxonomic classification.

## Usage
### download_genomes.sh
Download accessions using NCBI command line tool to get paired end reads for each accession
Merge paired end reads using USEARCH
Pass each merged reads file into ART to create ~10000 simulated reads per accession, ~1 000 000 reads in total

### Refseq.ipynb
Get a list of accessions for a genus (pseudomonas) from RefSEQ database (refseq.txt)
Filter out accessions that are present in Kraken2 (prevents bias) but where the species is present in the database (awareness)
20 species, select 5 accessions randomly per species = 100 accessions


## Citations
### Tools Used
- ART
- NCBI
- Kraken2
- Usearch
- DeepEC

## 