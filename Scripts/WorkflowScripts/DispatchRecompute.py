import os
import subprocess
import sys

def main():
    # Read inputs from environment variables or arguments
    number_of_runners = int(os.getenv('number_of_runners'))
    start_index = int(os.getenv('START_INDEX'))
    end_index = int(os.getenv('END_INDEX'))
    working_branch_name = os.getenv('BRANCH_NAME')

    # Check if end_index is -1, and set it to the last folder index based on the total count in info_files
    if end_index == -1:
        info_files_dir = 'Scripts/BuildDatabank/info_files'
        folders = [name for name in os.listdir(info_files_dir) if os.path.isdir(os.path.join(info_files_dir, name))]
        end_index = len(folders) - 1  # Set end_index based on the folder count
    
    
    # Calculate total number of items
    total_items = end_index - start_index + 1

    # Calculate base chunk size and remainder
    chunk_size = total_items // number_of_runners
    remainder = total_items % number_of_runners

    current_start = start_index

    for i in range(0, number_of_runners):
        # Calculate end index for this chunk
        current_chunk_size = chunk_size
        if i == 0:
            current_chunk_size += remainder

        current_end = current_start + current_chunk_size - 1

        print(f"Dispatching child workflow for indices {current_start} to {current_end}")

        try:
            # Run the GitHub CLI command to dispatch the workflow
            result = subprocess.run([
                "gh", "workflow", "run", "RecomputeInstance.yml", "--ref", "dev_pipeline_compose",
                "--field", f"working_branch_name={working_branch_name}",
                "--field", f"start_index={current_start}",
                "--field", f"end_index={current_end}"
            ], check=True, capture_output=True, text=True)
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error dispatching workflow: {e}")
            print(f"Command output: {e.output}")
            print(f"Command stderr: {e.stderr}")
        current_start = current_end + 1


if __name__ == "__main__":
    main()
