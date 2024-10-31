#!/bin/bash

DATABANK_ABS_PATH=$(pwd)
ORDERPARAMETERS_DIR="Data/experiments/OrderParameters"
FORMFACTOR_DIR="Data/experiments/FormFactors"
cd "$ORDERPARAMETERS_DIR" || exit

git fetch origin $BRANCH_NAME
git pull origin $BRANCH_NAME
cd $DATABANK_ABS_PATH

# Find new added orderparameter files in this branch relative to the other branch mentioned here:
NEW_ORDERPARAMETER_FILES=$(git diff --name-only origin/$BRANCH_NAME origin/$TARGET_BRANCH -- $ORDERPARAMETERS_DIR)
cd $ORDERPARAMETERS_DIR
if [ -n "$NEW_ORDERPARAMETER_FILES" ]; then  
  for file in $NEW_ORDERPARAMETER_FILES; do
    if [[ $file == *.dat ]]; then
      echo "Running data_to_json.py for $file"
      python3 "data_to_json.py" "$DATABANK_ABS_PATH/$file"
    fi
  done
else
  echo "No new files detected in $ORDERPARAMETERS_DIR."
fi
cd $DATABANK_ABS_PATH

# Find new added formfactor files in this branch relative to the other branch mentioned here:
NEW_FORMFACTOR_FILES=$(git diff --name-only origin/$BRANCH_NAME origin/$TARGET_BRANCH -- $FORMFACTOR_DIR)
if [ -n "$NEW_FORMFACTOR_FILES" ]; then  
  for file in $NEW_FORMFACTOR_FILES; do
    if [[ $file == *.dat || $file == *.xff ]]; then
      echo "Running data_to_json.py for formfactor files: $file"
      python3 "data_to_json.py" "$DATABANK_ABS_PATH/$file"
    fi
  done
else
  echo "No new files detected in $FORMFACTOR_DIR."
fi

cd "$DATABANK_ABS_PATH" 
git pull 
git status 
git add .
git commit -m "Automated push by NREC with new experiment data"
git push https://x-access-token:$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git
