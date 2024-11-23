import os
from DatabankLib.core import initialize_databank  # Replace with your actual module name
from DatabankLib import NMLDB_ROOT_PATH, NMLDB_SIMU_PATH

# Initialize the databank
systems = initialize_databank()
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
