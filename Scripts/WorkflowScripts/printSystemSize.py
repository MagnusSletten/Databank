import os
from DatabankLib.core import initialize_databank

"""
Temporary convenience method to just retrieve the smallest files
"""

def find_smallest_files(systems, n):
    """
    Finds the smallest n systems based on their TRAJECTORY_SIZE and returns their original indexes.
    """
    if not systems:
        print("No systems available.")
        return []

    # Attach the original index to each system for tracking
    indexed_systems = [(i, system) for i, system in enumerate(systems)]

    # Sort systems by TRAJECTORY_SIZE
    sorted_systems = sorted(indexed_systems, key=lambda x: x[1].get("TRAJECTORY_SIZE", float("inf")))

    # Return the smallest n systems and their original indexes
    return sorted_systems[:n]

# Initialize the databank
systems = list(initialize_databank())
systems.sort(key=lambda x: x["path"])  # Sort systems by path

# Fetch the START_INDEX from the environment variable
start_index = os.getenv("START_INDEX")

if start_index is not None:
    # Convert START_INDEX to an integer
    try:
        start_index = int(start_index)
        print(systems[start_index]["TRAJECTORY_SIZE"])
    except (ValueError, IndexError):
        print(f"Invalid START_INDEX: {start_index}. Ensure it's a valid integer within range.")
else:
    print("START_INDEX environment variable is not set.")

# Fetch the number of smallest files to print from an environment variable or default
num_smallest_files = int(os.getenv("NUM_SMALLEST_FILES", 5))  # Default to 5

# Find and print the smallest n files
smallest_files = find_smallest_files(systems, num_smallest_files)

print(f"Smallest {num_smallest_files} files:")
for original_index, file_info in smallest_files:
    print(f"Index: {original_index}, TRAJECTORY_SIZE: {file_info.get('TRAJECTORY_SIZE', 'N/A')}")
