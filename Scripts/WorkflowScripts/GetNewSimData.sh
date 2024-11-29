#!/bin/bash

#Needs to be run from the root of the repository for now. 

# Directory path:
TARGET_DIR="Scripts/BuildDatabank/info_files"

# Path to AddData.py:
ADD_DATA_SCRIPT="Scripts/BuildDatabank/AddData.py"

# Store absolute paths for later use:
DATABANK_ABS_PATH=$(pwd)
cd "$TARGET_DIR"
TARGET_DIR_ABS=$(pwd)
cd "$DATABANK_ABS_PATH/Scripts/BuildDatabank"
BUILDDATABANKPATH=$(pwd)

# Fetch the latest changes from the branches:
git pull origin "$BRANCH_NAME" || { echo "git pull failed"; exit 1; }

# Create a single work directory before processing all files:
WORK_DIR="/tmp/databank_workdir"
mkdir -p "$WORK_DIR" || { echo "Failed to create work directory"; exit 1; }

# Find new added files in this branch relative to the target branch:
NEW_FILES=$(git diff --name-status origin/"$BRANCH_NAME" origin/"$TARGET_BRANCH" | grep "info_files" | awk '{print $2}')
cd "$BUILDDATABANKPATH"

# If new files exist:
if [ -n "$NEW_FILES" ]; then
  echo "$NEW_FILES"
  # Run AddData.py for each new file listed in the output:
  for file in $NEW_FILES; do
    if [[ $file == *.yaml ]]; then
      echo "Running AddData.py for $file"
      python3 "AddData.py" -f "$DATABANK_ABS_PATH/$file" -w "$WORK_DIR" || { echo "AddData.py failed"; exit 1; }
    fi
  done
else
  echo "No new files detected in $TARGET_DIR."
fi

cd "$DATABANK_ABS_PATH/Scripts/AnalyzeDatabank"
./calcProperties.sh || { echo "calcProperties.sh failed"; exit 1; }

cd "$BUILDDATABANKPATH"
python searchDATABANK.py || { echo "searchDATABANK.py failed"; exit 1; }
python QualityEvaluation.py || { echo "QualityEvaluation.py failed"; exit 1; }
python makeRanking.py || { echo "makeRanking.py failed"; exit 1; }



# Push changes to the repository:
cd "$DATABANK_ABS_PATH"
git status


git add Data/Simulations/*/*/*/*/README.yaml
git add Data/Simulations/*/*/*/*/apl.json
git add Data/Simulations/*/*/*/*/*OrderParameters.json
git add Data/Simulations/*/*/*/*/FormFactor.json
git add Data/Simulations/*/*/*/*/TotalDensity.json
git add Data/Simulations/*/*/*/*/thickness.json
git add Data/Simulations/*/*/*/*/eq_times.json
git add Data/Simulations/*/*/*/*/*OrderParameters_quality.json
git add Data/Simulations/*/*/*/*/FormFactorQuality.json
git add Data/Simulations/*/*/*/*/*FragmentQuality.json
git add Data/Simulations/*/*/*/*/SYSTEM_quality.json

git commit -m "Automated push by NREC with new simulation data" || { echo "git commit failed"; exit 1; }
git push https://x-access-token:$GITHUB_TOKEN@github.com/$REPO_NAME.git || { echo "git push failed"; exit 1; }
