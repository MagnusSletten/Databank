from DatabankLib.core import initialize_databank 
import subprocess
import sys
import os


"""
Contains methods used for python scripts related to workflows. 
"""

#Helper to run a shell command and exit on failure. Optional work directory can be applied.
def run_command(command, error_message="Command failed", working_dir=None):
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_dir)
    except subprocess.CalledProcessError:
        print(error_message)
        sys.exit(1)

#Run a Python script using the current interpreter (sys.executable). Optional work directory can be applied.
def run_python_script(script_path, args=None, error_message="Python script failed", working_dir=None):
    if args is None:
        args = []
    try:
        subprocess.run(
            [sys.executable, script_path, *args],
            check=True,
            cwd=working_dir  # Set working directory if provided
        )
    except subprocess.CalledProcessError:
        print(error_message)
        sys.exit(1)

#TODO: Use package paths directly instead of this dictionary approach. 
def get_databank_paths(NMLDB_ROOT_PATH):
    Builddatabank_path = os.path.join(NMLDB_ROOT_PATH, "Scripts", "BuildDatabank")
    AddData_path = os.path.join(Builddatabank_path, "AddData.py")
    AnalyzeDatabank_path = os.path.join(NMLDB_ROOT_PATH, "Scripts", "AnalyzeDatabank")
    calcProperties_path = os.path.join(AnalyzeDatabank_path, "calcProperties.sh")
    searchDATABANK_path = os.path.join(Builddatabank_path, "searchDATABANK.py")
    QualityEvaluation_path = os.path.join(Builddatabank_path, "QualityEvaluation.py")
    makeRanking_path = os.path.join(Builddatabank_path, "makeRanking.py")

    return {
        "Builddatabank_path": Builddatabank_path,
        "AddData_path": AddData_path,
        "AnalyzeDatabank_path": AnalyzeDatabank_path,
        "calcProperties_path": calcProperties_path,
        "searchDATABANK_path": searchDATABANK_path,
        "QualityEvaluation_path": QualityEvaluation_path,
        "makeRanking_path": makeRanking_path
    }


def get_infofile_path_from_folder(folder_path):
    """
    Return the first .yaml or .yml filepath in the given folder,
    or None if the folder doesn't exist or contains no matching files.
    """
    try:
        for fname in os.listdir(folder_path):
            if fname.lower().endswith(('.yaml', '.yml')):
                return os.path.join(folder_path, fname)
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    return None
            
       
def delete_info_file(info_file_path):
    try:
        os.remove(info_file_path)
        print(f"Deleted info file: {info_file_path}")
    except OSError as e:
        print(f"Warning: could not delete {info_file_path}: {e}")