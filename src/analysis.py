import pandas as pd
import sys
import re
from Bio import SeqIO
from pathlib import Path

# Global variables
CLASSIFIED = "is_classified"
SEQ_ID = "seq_id"
TAX_ID = "taxon_id"
BP_LENGTH = "bp_length"
LCA_MAPPING = "LCA_mapping"

def calculate_score(self, index: int) -> float:
    """
    Calculates the confidence score of taxonomic assignment to a sequence by
    dividing the number of k-mers mapped to a taxon by the total number of 
    k-mers from that sequence.

    Args:
        index (int): an index into the kraken2 output DataFrame, where each 
            index corresponds to a sequence
    """
    tax_id = k2_output["taxon_id"][index]
    seq_id = k2_output["seq_id"][index]
    print("Assigned ID:", tax_id)
    lca_mapping = k2_output["LCA_mapping"][index]
    mappings = lca_mapping.split()
    print("Mappings:", mappings)
    total = 0
    match_total = 0
    # loop over LCA mappings for this particular sequence
    for mapping in mappings:
        query = fr'([0-9]*):([0-9]*)'
        match = re.match(query, mapping) # use regex match to find query mapping
        q_id = match.group(1)
        kmer_count = int(match.group(2))
        # we want to calculate the confidence score this assignment to the taxon_id
        if int(tax_id) == int(q_id):
            total += kmer_count
            match_total += kmer_count
        else:
            total += kmer_count
    score = match_total/total
    print(f"Score for sequence {seq_id} assigned to taxon {tax_id}:", score)
    return score


def fastq_to_dataframe(fastq_file):
    data = {
        'seq_id': [],
        'sequence': [],
        'bp_length': []
    }

    for record in SeqIO.parse(fastq_file, "fastq"):
        data['seq_id'].append(record.id)
        data['sequence'].append(str(record.seq))
        data['bp_length'].append(len(record.seq))

    df = pd.DataFrame(data)
    return df


def fasta_to_dataframe(fasta_file):
    data = {
        'seq_id': [],
        'sequence': [],
        'bp_length': []
    }

    for record in SeqIO.parse(fasta_file, "fasta"):
        data['seq_id'].append(record.id)
        data['sequence'].append(str(record.seq))
        data['bp_length'].append(len(record.seq))

    df = pd.DataFrame(data)
    return df


def main():
    pass

if __name__ == '__main__':
    arg_count = len(sys.argv)
    # generate a pandas dataframe from our kraken2 report, delimited by tab ('\t')
    k2_report_file = "/home/j/jparkin/wongkoji/final_pipeline/example_data/pm_mtx.kreport2"
    kraken_out_file = "/home/j/jparkin/wongkoji/final_pipeline/example_data/pm_mtx_kraken.out"
    fastq_file_path = "/scratch/j/jparkin/wongkoji/data/pm_merged.fq"
    fasta_file_path = "/home/j/jparkin/wongkoji/data/merged_paired_mtx.fasta"

    report_df = pd.read_csv(filepath_or_buffer=k2_report_file, 
                            sep='\t',
                            names=["%_clade", "#_clade_frags", "#_taxon_frags", "class", "ncbi_taxon_id", "name"])

    # Added a header explaining each column of the data.

    # %_clade: Percentage of fragments covered by the clade rooted at this taxon
    # #_clade_frags: Number of fragments covered by the clade rooted at this taxon
    # #_taxon_frags: Number of fragments assigned directly to this taxon
    # class: A rank code indicating (U)nclassified, (R)oot, (D)omain, (K)ingdom, (P)hylum, (C)lass, (O)rder, (F)amily, (G)enus, (S)pecies.
    # taxon_id: The Taxonomic ID number from NCBI
    # name: scientific name of taxon

    # extract k-mer count information corresponding to data in stdout in kraken.out
    k2_output = pd.read_csv(filepath_or_buffer=kraken_out_file, 
                            sep='\t',
                            names=[CLASSIFIED, SEQ_ID, TAX_ID, BP_LENGTH, LCA_MAPPING])

    # create a map of taxon_id to seq_ids
    seq_by_taxon = k2_output.groupby(TAX_ID)[SEQ_ID].apply(list).to_dict()

    fasta_file_path = "/home/j/jparkin/wongkoji/data/merged_paired_mtx.fasta"
    fasta_df = fasta_to_dataframe(fasta_file_path)
    fasta_df = fastq_to_dataframe(fastq_file_path)
