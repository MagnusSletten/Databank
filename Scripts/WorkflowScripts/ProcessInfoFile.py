from DatabankLib import NMLDB_SIMU_PATH
from DatabankLib import NMLDB_ROOT_PATH
from .Workflow_utils import *  

import os 
import argparse

def main(info_file_path):
    
    NMRLB_BUILDDATAPANK_PATH = os.path.join(NMLDB_ROOT_PATH,"Scripts","BuildDatabank")
    AddData_path = os.path.join(NMRLB_BUILDDATAPANK_PATH,"AddData.py")
    calcProperties_path = os.path.join(NMLDB_ROOT_PATH,"Scripts","AnalyzeDatabank","calcProperties.sh")
    searchDATABANK_path = os.path.join(NMRLB_BUILDDATAPANK_PATH,"searchDATABANK.py")
    QualityEvaluation_path = os.path.join(NMRLB_BUILDDATAPANK_PATH,"QualityEvaluation.py")
    makeRanking_path = os.path.join(NMRLB_BUILDDATAPANK_PATH,"makeRanking.py")

    WORK_DIR="/tmp/databank_workdir"
    os.makedirs(WORK_DIR, exist_ok=True)
    add_data_args = ["-f",info_file_path,"-w", WORK_DIR]

    run_python_script(AddData_path,add_data_args,error_message="AddData failed")

    run_command(calcProperties_path, "Calcproperties failed")

    run_python_script(searchDATABANK_path,error_message="SearchDatabank failed")
    run_python_script(QualityEvaluation_path,error_message= "QualtyEvaluation failed")
    run_python_script(makeRanking_path,error_message="makeRanking failed")

    add_sim_files()

    git_commit("Automated push with new simulation data")
  

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
    parser.add_argument("info_file", help="Path to the info.yaml file")

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args.info_file)
