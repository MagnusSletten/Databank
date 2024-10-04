import os
import subprocess
import sys

def main():
    # Read inputs from environment variables or arguments
    number_of_runs = int(os.getenv('NUMBER_OF_RUNS'))
    start_index = int(os.getenv('START_INDEX'))
    end_index = int(os.getenv('END_INDEX'))
    working_branch_name = os.getenv('WORKING_BRANCH_NAME')
    
    # Calculate total number of items
    total_items = end_index - start_index + 1

    # Calculate base chunk size and remainder
    chunk_size = total_items // number_of_runs
    remainder = total_items % number_of_runs

    current_start = start_index

    for i in range(0, number_of_runs):
        # Calculate end index for this chunk
        current_chunk_size = chunk_size
        if i == 0:
            current_chunk_size += remainder

        current_end = current_start + current_chunk_size - 1

        print(f"Dispatching child workflow for indices {current_start} to {current_end}")

        try:
            # Run the GitHub CLI command to dispatch the workflow
            result = subprocess.run([
                "gh", "workflow", "run", "RecomputeInstance.yml", "--ref", "main",
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
