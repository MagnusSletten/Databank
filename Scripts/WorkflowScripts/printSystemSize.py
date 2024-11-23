import os
from DatabankLib.core import initialize_databank  # Replace with your actual module name
from DatabankLib import NMLDB_ROOT_PATH, NMLDB_SIMU_PATH

def find_smallest_file_index(systems):
    """
    Finds the index of the system with the smallest trajectory size in the sorted list.
    """
    if not systems:
        print("No systems available.")
        return None

    # Find the index of the system with the smallest TRAJECTORY_SIZE
    smallest_index = min(range(len(systems)), key=lambda i: systems[i].get("TRAJECTORY_SIZE", float("inf")))
    return smallest_index



# Initialize the databank
systems = list(initialize_databank()) 
systems.sort(key=lambda x: x["path"])

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


print(f"Smallest file is at index {find_smallest_file_index(systems)}")