import os
import subprocess
import sys
from DatabankLib.core import initialize_databank


#Random change to test pipeline
#Random change 2.3.

def main():
    # Read inputs from environment variables
    number_of_runners = int(os.getenv('NUMBER_OF_RUNNERS', 1))  # Default to 1 runner
    start_index = int(os.getenv('START_INDEX', 0))  # Default start index to 0
    end_index = int(os.getenv('END_INDEX', -1))  # Default end index to -1 (must be set)
    working_branch_name = os.getenv('BRANCH_NAME', 'main')  # Default branch name to 'main'

    # Initialize databank to retrieve systems
    systems = initialize_databank()
    total_systems = len(systems)

    #If the ending index is set to -1 it will default to using all files to the end
    if(end_index ==-1):
        end_index = total_systems-1


    # Validate range of indices
    if start_index < 0 or end_index >= total_systems:
        raise IndexError(f"Start or end index is out of range. Valid range is 0 to {total_systems - 1}.")
    if end_index < start_index:
        raise ValueError("END_INDEX must be greater than or equal to START_INDEX.")

    # Calculate total number of items
    total_items = end_index - start_index + 1

    # Calculate base chunk size and remainder
    chunk_size = total_items // number_of_runners
    remainder = total_items % number_of_runners

    current_start = start_index

    for i in range(0, number_of_runners):
        # Calculate end index for this chunk
        current_chunk_size = chunk_size
        if i < remainder:
            current_chunk_size += 1  # Distribute remainder to the first chunks

        current_end = current_start + current_chunk_size - 1

        print(f"Dispatching child workflow for indices {current_start} to {current_end}")

        try:
            # Run the GitHub CLI command to dispatch the workflow
            result = subprocess.run([
                "gh", "workflow", "run", "RecomputeInstance.yml", "--ref", "dev_cicd",
                "--field", f"working_branch_name={working_branch_name}",
                "--field", f"start_index={current_start}",
                "--field", f"end_index={current_end}"
            ], check=True, capture_output=True, text=True)
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error dispatching workflow for indices {current_start}-{current_end}: {e}")
            print(f"Command output: {e.output}")
            print(f"Command stderr: {e.stderr}")

        # Update the start index for the next chunk
        current_start = current_end + 1


if __name__ == "__main__":
    main()
