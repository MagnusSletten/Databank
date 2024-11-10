#!/bin/bash

# Directory path:
TARGET_DIR="Scripts/BuildDatabank/info_files"


# Path to AddData.py:
ADD_DATA_SCRIPT="Scripts/BuildDatabank/AddData.py"

# Store absolute paths for later use:
DATABANK_ABS_PATH=$(pwd)
cd "$TARGET_DIR"
TARGET_DIR_ABS=$(pwd)
cd "$DATABANK_ABS_PATH/Scripts/BuildDatabank/"
BUILDDATABANKPATH=$(pwd)

# Fetch the latest changes from the branches:
git fetch origin "$BRANCH_NAME" || { echo "git fetch failed"; exit 1; }
git pull origin "$BRANCH_NAME" || { echo "git pull failed"; exit 1; }

# Create a single work directory before processing all files:
WORK_DIR="/tmp/databank_workdir"
mkdir -p "$WORK_DIR" || { echo "Failed to create work directory"; exit 1; }

# Get list of all .yaml files and sort by numeric folder names
sorted_files=($(find "$BUILDDATABANKPATH/info_files" -name "*.yaml" | sort -V))

# Calculate the subset of files based on $start_index and $end_index
subset_files=("${sorted_files[@]:$start_index:$(($end_index - $start_index + 1))}")

# Initialize an array to store failed files
failed_files=()

# Process each file in the subset
for file in "${subset_files[@]}"; do
  if [[ $file == *.yaml ]]; then
    folder=$(dirname "$file") 
    echo "Running AddData.py for $file in folder $folder"
    cd "$BUILDDATABANKPATH"
    
    # Run AddData.py and check if it fails
    if ! python3 "AddData.py" -f "$file" -w "$WORK_DIR"; then
      echo "AddData.py failed for $file"
      failed_files+=("$file")  # Add the filename to the failed_files list
    fi
  fi
done

cd "$DATABANK_ABS_PATH"
git pull
# After the loop, log all failed files with a single timestamp if there are any
if [ ${#failed_files[@]} -ne 0 ]; then
  timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$timestamp - The following files failed to process:" >> Data/Logs/recomputeLogs.txt
  for failed_file in "${failed_files[@]}"; do
    echo "$failed_file" >> Data/Logs/recomputeLogs.txt
    echo "$failed_file"  # Optionally, print to console as well
  done
else
  echo "All files processed successfully."
fi


# If no new files were detected
if [[ ${#subset_files[@]} -eq 0 ]]; then
  echo "No new files detected in $BUILDDATABANKPATH for the specified range."
fi


git status
git pull
git add Data/Logs/*
git add Data/Simulations/*/*/*/*/README.yaml
git commit -m "Files recomputed" || { echo "git commit failed"; exit 1; }
git push https://x-access-token:$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git || { echo "git push failed"; exit 1; }
