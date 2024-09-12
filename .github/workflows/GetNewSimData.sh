#!/bin/bash

# Directory path:
TARGET_DIR="Scripts/BuildDatabank/info_files"

#The branch we are comparing to. For final build this will be the branch the user opens merge requests to:
TARGET_BRANCH="docker_test"

GITHUB_USERNAME="MagnusSletten_Bot"  
GITHUB_EMAIL="magnus.elias.sletten@gmail.com"  


git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_EMAIL"


# Name of file we're going to store new filenames in: 
OUTPUT_FILE="new_files.txt"

# Path to the AddData:
ADD_DATA_SCRIPT="Scripts/BuildDatabank/AddData.py"

#Makes the output file:
> $OUTPUT_FILE

DATABANK_ABS_PATH=$(pwd)
cd $TARGET_DIR
TARGET_DIR_ABS=$(pwd)
cd $DATABANK_ABS_PATH
cd Scripts/BuildDatabank

git fetch origin

#Finding new added files in this branch relative to the other branch meantioned here:
NEW_FILES=$(git diff --name-status origin/$BRANCH_NAME origin/$TARGET_BRANCH | grep "info_files" | awk '{print $2}')


# If new files is not Null:
if [ -n "$NEW_FILES" ]; then
  echo "$NEW_FILES"
  echo "$NEW_FILES" > "$OUTPUT_FILE"  
  
  # Run AddData.py for each new file listed in the output file::
  while IFS= read -r file; do
    
    echo "Running AddData.py for $file"
    python3 "AddData.py" -f "$DATABANK_ABS_PATH/$file"
    break   
  done < "$OUTPUT_FILE"

else
  echo "No new files detected in $TARGET_DIR."
fi

cd $DATABANK_ABS_PATH
git status 
git add .
git commit -m "Automated push test"
git push 