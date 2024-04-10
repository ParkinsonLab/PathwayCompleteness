import pandas as pd
import Bio
import os
import json


def clean_ec_data(ec_number):
    """Clean EC formatting. EC must be in format 'EC:#.#.#.#' """
    if not ec_number:
        return "None"
    if '-' in ec_number:
        return "None"
    # TODO: split these
    elif ';' in ec_number:
        return "None"
    else:
        return ec_number


def get_pathways(ec_id, df: pd.DataFrame):
    """get a list of pathways given an EC number in format ec:#.#.#.#"""
    if "ec:" not in ec_id:
        raise NameError
    return list(df[df['ec'] == ec_id]['pathway'])


def get_enzymes(pathway_id, df: pd.DataFrame):
    """get a list of enzymes given a KEGG pathway in format ec#####"""
    return list(df[df['pathway'] == pathway_id]['ec']) 


def find_pathways_opt(ec_number, ec_pathways_dict, paths_to_ec_df):
    """Finds pathways an enzyme is present

    Args:
        ec_number (str): must be a valid Enzyme Commission number

    Returns:
        list of pathways
    """
    if 'ec' not in ec_number:
        ec_number = f"ec:{ec_number}"
    pathways = get_pathways(ec_number, paths_to_ec_df)
    for path in pathways:
        if path not in ec_pathways_dict:
            ec_pathways_dict[path] = [ec_number]
        else:
            ec_pathways_dict[path].append(ec_number)
    return ec_pathways_dict


def calculate_pathway_completeness(pathway_of_interest, ec_pathways, paths_to_ec_df: pd.DataFrame):
    if pathway_of_interest not in ec_pathways:
        print(f"Pathway {pathway_of_interest} not present in dictionary.")
        return
    if pathway_of_interest not in list(paths_to_ec_df['pathway']):
        print(f"Pathway {pathway_of_interest} not present in DataFrame.") 
        return
    
    # Get the list of EC numbers involved in the pathway of interest
    total_enzymes = set(get_enzymes(pathway_of_interest, paths_to_ec_df))
    present_enzymes = list(set(ec_pathways[pathway_of_interest]))
    # print(present_enzymes)
    
    try:
        completeness = len(present_enzymes) / len(total_enzymes)
        return completeness
    except ZeroDivisionError as e:
        print(pathway_of_interest)
        print("division by zero, is the pathway of interest formatted correctly? (eg. 'ec00300')")
        return
    
# brute force
def calculate_all_paths_completeness(ec_pathways_dict, paths_to_ec_df):
    pathway_completeness = {}
    for path in ec_pathways_dict:
        if path not in pathway_completeness:
            pathway_completeness[path] = calculate_pathway_completeness(path, ec_pathways_dict, paths_to_ec_df)
    return pathway_completeness


def main():
    return

if __name__ == '__main__':
    # Get the current working directory
    current_dir = os.getcwd()
    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)
    print("Parent Directory:", parent_dir)
    
    paths_to_ec_df = pd.read_csv(os.path.join(parent_dir, "db/pathways_ecs.csv"))
    
    # creating a df for our ecs
    enzymes_file = os.path.join(parent_dir, "db/enzymes_ec.tsv")
    enzymes_df = pd.read_csv(enzymes_file, delimiter='\t', names=["ec", "name"])
    # creating a df for our pathways
    pathways_file = os.path.join(parent_dir, "db/pathways_ec.tsv")
    pathways_df = pd.read_csv(pathways_file, delimiter='\t', names=["pathway", "function"])
    
    # TODO: make this deepec_file an input
    deepec_file = "/scratch/j/jparkin/wongkoji/deepec_outputs/deepEC_321846/DeepECv2_result.txt"
    deepec_df = pd.read_csv(deepec_file, sep='\t')
    print(len(deepec_df))
    
    # Drop any unannotated reads
    deepec_df = deepec_df[deepec_df['prediction'] != 'None']
    deepec_df['prediction'] = deepec_df['prediction'].apply(clean_ec_data)

    # format ECs with lowercase for KEGG API
    deepec_df['prediction'] = deepec_df['prediction'].apply(str.lower)


    present_enzymes = list(set(deepec_df['prediction']))
    ec_pathways_dict = {}
    for ec in present_enzymes:
        ec_pathways_dict = find_pathways_opt(ec, ec_pathways_dict, paths_to_ec_df)
    completeness = calculate_all_paths_completeness(ec_pathways_dict, paths_to_ec_df)
    
    # convert completeness to a dataframe which we can export as a csv
    completeness_df = pd.DataFrame(list(completeness.items()), columns=['pathway', 'completeness'])
    completeness_df.to_csv(os.path.join(parent_dir, "output/321846_pathway_completeness.csv"), index=False)