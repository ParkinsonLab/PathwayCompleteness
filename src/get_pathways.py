import json
import pandas as pd
import os

# this file was used to generate our db, specifically pathways.json and pathways_ecs.csv

def get_pathways(ec_id, df: pd.DataFrame):
    """get a list of pathways given an EC number in format ec:#.#.#.#"""
    if "ec:" not in ec_id:
        raise NameError
    return list(df[df['ec'] == ec_id]['pathway'])

def get_enzymes(pathway_id, df: pd.DataFrame):
    """get a list of enzymes given a KEGG pathway in format ec#####"""
    return list(df[df['pathway'] == pathway_id]['ec']) 

def append_ecs(pathway_id):
    # Retrieve information about enzymes involved in the pathway
    enzymes = get_enzymes(pathway_id, paths_to_ec_df)
    ecs_per_path[pathway_id] = enzymes


if __name__ == "__main__":
    # Get the current working directory
    current_dir = os.getcwd()

    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)

    pathways_file = os.path.join(parent_dir, "db/pathways_ec.tsv")
    pathways_df = pd.read_csv(pathways_file, delimiter='\t', names=["pathway", "function"])
    # https://rest.kegg.jp/link/pathway/ec:1.1.1.3 
    ecs_per_path = {}

    # run append_ecs function on all the values of pathway
    pathways_df['pathway'].apply(append_ecs)
    with open("pathways.json", "w") as outfile:
        json.dump(ecs_per_path, outfile)

    json_file = open(os.path.join(parent_dir, "db/pathways.json"), "r")
    ec_paths = json.load(json_file)

    rows = [(key, value) for key, values in ec_paths.items() for value in values]
    paths_to_ec_df = pd.DataFrame(rows, columns=['pathway', 'ec'])
    paths_to_ec_df.head()

    # save pathways to a csv
    paths_to_ec_df.to_csv(os.path.join(parent_dir, "db/pathways_ecs.csv"))