#!/bin/bash

# Update the repository to ensure it’s up to date
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "$BRANCH_NAME" || { echo "Failed to check out branch $BRANCH_NAME"; exit 1; }

python Scripts/DockerScripts/DispatchRecompute.py || { echo "Dispatch Recompute failed"; exit 1; }