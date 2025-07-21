from DatabankLib.core import initialize_databank  # adjust import as needed
import numpy as np

# Load all systems
systems = initialize_databank()

# Extract the TRAJECTORY_SIZE values (in bytes, or whatever unit you store)
sizes = []
larger = 0
max = 0 
for sys in systems:
    size = sys.readme.get("TRAJECTORY_SIZE")
    if size is not None:
        if size > 13665707252:
            larger += 1
        if size > max:
            max = size 
        sizes.append(size)

if not sizes:
    print("No trajectory size data found.")
else:
    mean_size = np.mean(sizes)
    print(f"Computed mean trajectory size over {len(sizes)} systems: {mean_size:.2f}")
    print(f"There are {larger} files larger")
    print(f"Max size {max}")