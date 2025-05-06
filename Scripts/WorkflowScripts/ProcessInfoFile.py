from DatabankLib import NMLDB_SIMU_PATH
from DatabankLib import NMLDB_ROOT_PATH
from .Workflow_utils import *  

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
    

def run_addData_for_files(folder_path,info_files,work_directory):
    path_dict = get_databank_paths(NMLDB_ROOT_PATH)
    for file in info_files:
        file_path = os.path.join(folder_path,file)
        add_data_args = ["-f", file_path, "-w", work_directory]
        run_python_script(path_dict["AddData_path"], add_data_args, error_message="AddData failed")






def add_sim_files():
    run_command("git add Data/Simulations/*/*/*/*/README.yaml")
    run_command("git add Data/Simulations/*/*/*/*/apl.json")
    run_command("git add Data/Simulations/*/*/*/*/*OrderParameters.json")
    run_command("git add Data/Simulations/*/*/*/*/FormFactor.json")
    run_command("git add Data/Simulations/*/*/*/*/TotalDensity.json")
    run_command("git add Data/Simulations/*/*/*/*/thickness.json")
    run_command("git add Data/Simulations/*/*/*/*/eq_times.json")
    run_command("git add Data/Simulations/*/*/*/*/*OrderParameters_quality.json")
    run_command("git add Data/Simulations/*/*/*/*/FormFactorQuality.json")
    run_command("git add Data/Simulations/*/*/*/*/*FragmentQuality.json")
    run_command("git add Data/Simulations/*/*/*/*/SYSTEM_quality.json")


def get_args():
    parser = argparse.ArgumentParser(description="Run NMRLipids data pipeline on a YAML info file.")
    parser.add_argument("info_file_folder", help="Path to the info.yaml file")

    return parser.parse_args()


#TODO: Use package paths directly instead of this dictionary approach. 

def get_databank_paths(NMLDB_ROOT_PATH):
    NMRLB_BUILDDATAPANK_PATH = os.path.join(NMLDB_ROOT_PATH, "Scripts", "BuildDatabank")
    AddData_path = os.path.join(NMRLB_BUILDDATAPANK_PATH, "AddData.py")
    AnalyzeDatabank_path = os.path.join(NMLDB_ROOT_PATH, "Scripts", "AnalyzeDatabank")
    calcProperties_path = os.path.join(AnalyzeDatabank_path, "calcProperties.sh")
    searchDATABANK_path = os.path.join(NMRLB_BUILDDATAPANK_PATH, "searchDATABANK.py")
    QualityEvaluation_path = os.path.join(NMRLB_BUILDDATAPANK_PATH, "QualityEvaluation.py")
    makeRanking_path = os.path.join(NMRLB_BUILDDATAPANK_PATH, "makeRanking.py")

    return {
        "NMRLB_BUILDDATAPANK_PATH": NMRLB_BUILDDATAPANK_PATH,
        "AddData_path": AddData_path,
        "AnalyzeDatabank_path": AnalyzeDatabank_path,
        "calcProperties_path": calcProperties_path,
        "searchDATABANK_path": searchDATABANK_path,
        "QualityEvaluation_path": QualityEvaluation_path,
        "makeRanking_path": makeRanking_path
    }



if __name__ == "__main__":
    args = get_args()
    main(args.info_file_folder)
