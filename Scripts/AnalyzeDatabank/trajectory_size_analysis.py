from DatabankLib.core import initialize_databank  # adjust import as needed
import numpy as np

# Load all systems
systems = initialize_databank()

sizes = []
larger = 0
_max = 0

size_info = []  # Store (size, ID, path)

for sys in systems:
    size = sys.readme.get("TRAJECTORY_SIZE")
    if size is None:
        continue

    sizes.append(size)
    size_info.append((size, sys.readme.get("ID"), sys["path"]))

    if size > 13_665_707_252:
        larger += 1

    if size > _max:
        _max = size

if not sizes:
    print("No trajectory size data found.")
else:
    mean_size = np.mean(sizes)
    print(f"Computed mean trajectory size over {len(sizes)} systems: {mean_size:.2f}")
    print(f"There are {larger} files larger than 13_665_707_252")
    print(f"Max size: {_max}")
    print()
    print("5 smallest systems:")

    for size, id_, path in sorted(size_info)[:5]:
        print(f"  ID: {id_:<4}  Size: {size:<12}  Path: {path}")
