from DatabankLib.core import initialize_databank  # Replace with your actual module name
from DatabankLib import NMLDB_ROOT_PATH, NMLDB_SIMU_PATH


import os
import sys
import subprocess

def delete_json_files_for_system(system):
    """
    Deletes JSON files in the specified system's folder.
    """
    # Construct the full path
    system_path = os.path.join(NMLDB_SIMU_PATH, system["path"])
    print(f"Processing folder: {system_path}")

    # Delete JSON files in the system's folder
    try:
        for filename in os.listdir(system_path):
            if filename.endswith('.json'):
                file_path = os.path.join(system_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error processing {system_path}: {e}")
        raise


def run_calc_properties():
    """
    Change to the 'Scripts/AnalyzeDatabank' directory and run calcProperties.sh.
    """
    try:
        # Define the directory containing calcProperties.sh
        analyze_dir = os.path.join(NMLDB_ROOT_PATH,'Scripts', 'AnalyzeDatabank')

        # Change the working directory
        os.chdir(analyze_dir)
        print(f"Changed directory to: {os.getcwd()}")

        # Run the calcProperties.sh script
        print("Running calcProperties.sh...")
        subprocess.run(["bash", "calcProperties.sh"], check=True)
        print("calcProperties.sh executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running calcProperties.sh: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def git_commit_simulation_folder(folder_name,index):
    """
    Adds and commits changes for the specific simulation folder.
    """
    try:
        # Stage changes only for the specific folder
        subprocess.run(["git", "add", NMLDB_SIMU_PATH], check=True)

        # Commit changes
        commit_message = f"Processed simulation folder: {folder_name} at index: {index}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Committed changes: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git commit: {e}")
        raise

def pull_and_push_changes():
    """
    Pulls the latest changes and pushes new changes after processing.
    """
    try:
        print("Pulling latest changes...")
        subprocess.run(["bash", "PullPush.sh"], check=True)
        print("Changes pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during PullPush.sh: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    try: 
      
        # Retrieve indices as strings
        start_index_str = os.environ.get("START_INDEX")
        end_index_str = os.environ.get("END_INDEX")

        # Ensure indices are provided
        if start_index_str is None or end_index_str is None:
            raise ValueError("START_INDEX and END_INDEX environment variables must be set.")

        # Convert indices to integers
        start_index = int(start_index_str)
        end_index = int(end_index_str)

        # Initialize the databank and retrieve systems
        systems = initialize_databank()

        # Ensure the indices are within range
        if start_index < 0 or end_index >= len(systems):
            raise IndexError("Start or end index is out of range")

        # Process systems one by one
        for i in range(start_index, end_index + 1):
            print(f"Processing index {i}...")

            # Delete JSON files for the current system
            delete_json_files_for_system(systems[i])

            # Run calcProperties.sh after deleting files
            run_calc_properties()

            # Pull and push changes
            git_commit_simulation_folder(systems[i]["path"],i)
            pull_and_push_changes()

            print(f"Index {i} processed successfully.")

    except Exception as e:
        print(f"Error processing: {e}")
        sys.exit(1)