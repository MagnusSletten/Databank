from DatabankLib import NMLDB_SIMU_PATH
from DatabankLib import NMLDB_ROOT_PATH
from WorkflowScripts.Workflow_utils import *  


import os 
import argparse

def main(info_files_folder_path):    
    path_dict = get_databank_paths(NMLDB_ROOT_PATH)

    work_directory = "/tmp/databank_workdir"
    os.makedirs(work_directory, exist_ok=True)
    info_files = get_infofile_names_from_folder(info_files_folder_path)
    
    run_addData_for_files(info_files_folder_path,info_files,work_directory)
    run_command(
        path_dict["calcProperties_path"],
        "Calcproperties failed",
        working_dir=path_dict["AnalyzeDatabank_path"]
    )

    run_python_script(path_dict["searchDATABANK_path"], error_message="SearchDatabank failed")
    run_python_script(path_dict["QualityEvaluation_path"], error_message="QualityEvaluation failed")
    run_python_script(path_dict["makeRanking_path"], error_message="makeRanking failed")

    add_sim_files()
    stash_sim_files()
    

def run_addData_for_files(folder_path,info_files,work_directory):
    path_dict = get_databank_paths(NMLDB_ROOT_PATH)
    for file in info_files:
        file_path = os.path.join(folder_path,file)
        add_data_args = ["-f", file_path, "-w", work_directory]
        run_python_script(path_dict["AddData_path"], add_data_args, error_message="AddData failed")



def add_sim_files():
    patterns = [
        "*/*/*/*/README.yaml",
        "*/*/*/*/apl.json",
        "*/*/*/*/*OrderParameters.json",
        "*/*/*/*/FormFactor.json",
        "*/*/*/*/TotalDensity.json",
        "*/*/*/*/thickness.json",
        "*/*/*/*/eq_times.json",
        "*/*/*/*/*OrderParameters_quality.json",
        "*/*/*/*/FormFactorQuality.json",
        "*/*/*/*/*FragmentQuality.json",
        "*/*/*/*/SYSTEM_quality.json"
    ]

    for pattern in patterns:
        run_command(f"git add {NMLDB_SIMU_PATH}/{pattern}","Failed to add new simulation files")

def stash_sim_files():
        run_command("git stash push --keep-index -m 'simdata'", "Failed to stash new simulation files")

def get_args():
    parser = argparse.ArgumentParser(description="Run NMRLipids data pipeline on a YAML info file.")
    parser.add_argument("--info_file_folder", required=True, help="Path to the folder containing .yaml or .yml info files")

    return parser.parse_args()



if __name__ == "__main__":
    args = get_args()
    main(args.info_file_folder)
