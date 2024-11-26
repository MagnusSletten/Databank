"""
Recomputes JSON files starting from "start-index" and ending with "end-index", branch-name is an optional parameter and when included it will push to that branch. 

"""

from DatabankLib.core import initialize_databank  
from DatabankLib import NMLDB_ROOT_PATH, NMLDB_SIMU_PATH
import glob, os, sys, subprocess, argparse
import Workflow_utils


def delete_json_files_for_system(system):
    """
    Deletes JSON files in the specified system's folder.
    """
    # Construct the full path
    system_path = os.path.join(NMLDB_SIMU_PATH, system["path"])
    print(f"Processing folder: {system_path}", flush=True)

    # Delete JSON files in the system's folder
    try:
        for filename in os.listdir(system_path):
            if filename.endswith('.json'):
                file_path = os.path.join(system_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}", flush=True)
    except Exception as e:
        print(f"Error processing {system_path}: {e}", flush=True)
        raise


def run_calc_properties():
    """
    Change to the 'Scripts/AnalyzeDatabank' directory and run calcProperties.sh.
    """
    try:
        #AnalyzeDatabank directory:
        analyze_dir = os.path.join(NMLDB_ROOT_PATH,'Scripts', 'AnalyzeDatabank')
        os.chdir(analyze_dir)
        print(f"Changed directory to: {os.getcwd()}", flush=True)
        print("Running calcProperties.sh...", flush=True)
        subprocess.run(["bash", "calcProperties.sh"], check=True)
        print("calcProperties.sh executed successfully.", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running calcProperties.sh: {e}", flush=True)
        raise
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
        raise
def git_commit_simulation_folder(system):
    """
    Pulls the latest changes, adds only JSON files from the specific simulation folder, and commits changes.
    """
    try:
        os.chdir(NMLDB_ROOT_PATH)
        print("Pulling latest changes before committing...", flush=True)
        subprocess.run(["git", "pull"], check=True)
        print("Successfully pulled latest changes.", flush=True)
        folder_name = system["path"]
        json_files_dir = os.path.join("Data", "Simulations", folder_name)
        json_files_path = os.path.join("Data", "Simulations", folder_name, "*.json")
        matching_files = glob.glob(json_files_path)
        system_id = system["ID"]
        if not matching_files:
            print(f"No JSON files found in {json_files_path}. Skipping commit.", flush=True)
            return
        #Add new json files:
        subprocess.run(["git", "add"] + matching_files, check=True)
        #Add deletions of tracked .json files
        subprocess.run(["git", "add", "-u", json_files_dir], check=True)
        print(f"Staged JSON files: {matching_files}", flush=True)
        commit_message = f"Processed simulation with ID: {system_id}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Committed changes: {commit_message}", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Git pull or commit: {e}", flush=True)
        raise
    except Exception as e:
        print(f"Unexpected error during Git operations: {e}", flush=True)
        raise

def pull_and_push_changes():
    """
    Pulls the latest changes and pushes new changes after processing.
    """
    workflow_dir = os.path.join(NMLDB_ROOT_PATH, 'Scripts', 'WorkflowScripts')
    script_path = os.path.join(workflow_dir, "Git_Push.sh")
    try:
        print("Pulling latest changes...", flush=True)
        subprocess.run(["bash", script_path], check=True)
        print("Changes pushed successfully.", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Git_Push.sh execution: {e}", flush=True)
        raise
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process simulation data across systems.")
    parser.add_argument("--start-index", type=int, required=True, help="Start index for processing.")
    parser.add_argument("--end-index", type=int, required=True, help="End index for processing.")
    parser.add_argument("--branch-name", type=str, default=None, help="""Branch name for Git operations (optional). 
                        Git steps will be skipped if None""")


    args = parser.parse_args()

    try:
        print(f"This will recompute from {args.start_index} to {args.end_index}", flush=True)

        systems = Workflow_utils.sorted_databank()

        if args.start_index < 0 or args.end_index >= len(systems):
            raise IndexError("Start or end index is out of range")

        for i in range(args.start_index, args.end_index + 1):
            print(f"Processing index {i}...", flush=True)
            delete_json_files_for_system(systems[i])
            run_calc_properties()

            # Only run commit and push steps if a branch name is provided
            if args.branch_name:
                git_commit_simulation_folder(systems[i]["path"], i)
                pull_and_push_changes()

            print(f"Index {i} processed successfully.", flush=True)

    except Exception as e:
        print(f"Error processing: {e}", flush=True)
        sys.exit(1)
