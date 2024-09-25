#!/bin/bash

GITHUB_USERNAME="MagnusSletten_Bot"  
GITHUB_EMAIL="magnus.elias.sletten@gmail.com"  


git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_EMAIL"


# Name of file we're going to store new filenames in::
ORDERPARAMETER_FILE="orderparameters.txt"

#Makes the output file:
> $ORDERPARAMETER_FILE

DATABANK_ABS_PATH=$(pwd)
ORDERPARAMETERS_DIR=Data/experiments/OrderParameters
cd $ORDERPARAMETERS_DIR

git fetch origin $BRANCH_NAME
git pull origin $BRANCH_NAME

#Finding new added files in this branch relative to the other branch meantioned here:
NEW_ORDERPARAMETER_FILES=$(git diff --$ORDERPARAMETERS_DIR --name-status origin/$BRANCH_NAME origin/$TARGET_BRANCH | grep "info_files" | awk '{print $2}')


while IFS= read -r file; do
  # Check if the file is a .dat file
  if [[ "$file" == *.dat ]]; then
    echo "Running data_to_json.py for $file"
    python3 "data_to_json.py" -f "$DATABANK_ABS_PATH/$file"
    break   # Temporary for testing purposes.
  else
    echo "Skipping non-.dat file: $file"
  fi
done < "$ORDERPARAMETER_FILE"

else
  echo "No new files detected in $ORDERPARAMETERS."
fi




rm "$ORDERPARAMETER_FILE"

cd $DATABANK_ABS_PATH
git status 
git add .
git commit -m "Automated push by NREC"
git push 