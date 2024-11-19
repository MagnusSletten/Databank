from DatabankLib.core import initialize_databank  # Replace with your actual module name
from DatabankLib import NMLDB_SIMU_PATH  # Ensure this constant is accessible
import os
import sys 
import subprocess
def delete_json_files_in_range(start_index, end_index):
    # Initialize the databank and retrieve systems
    systems = initialize_databank()

    # Ensure the indices are within range
    if start_index < 0 or end_index > len(systems):
        raise IndexError("Start or end index is out of range")

    # Iterate over the specified range of systems
    for system in systems[start_index:end_index]:
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

def run_calc_properties():
    """
    Change to the 'Scripts/AnalyzeDatabank' directory and run calcProperties.sh.
    """
    try:
        # Define the directory containing calcProperties.sh
        analyze_dir = os.path.join('Scripts', 'AnalyzeDatabank')

        # Change the working directory
        os.chdir(analyze_dir)
        print(f"Changed directory to: {os.getcwd()}")

        # Run the calcProperties.sh script
        print("Running calcProperties.sh...")
        subprocess.run(["bash", "calcProperties.sh"], check=True)
        print("calcProperties.sh executed successfully.")
    
    except FileNotFoundError as fnfe:
        print(f"File not found: {fnfe}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running calcProperties.sh: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Get start and end indices from environment variables
        start_index = int(os.environ.get("START_INDEX", -1))
        end_index = int(os.environ.get("END_INDEX", -1))

        # Ensure indices are provided
        if start_index == -1 or end_index == -1:
            raise ValueError("START_INDEX and END_INDEX environment variables must be set.")

        # Call the delete method with the provided indices
        delete_json_files_in_range(start_index, end_index)

        # Run the calcProperties.sh script after deleting files
        run_calc_properties()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

