#!/bin/bash

# Pull latest changes
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "$BRANCH_NAME" || { echo "Failed to check out branch $BRANCH_NAME"; exit 1; }

python Scripts/WorkflowScripts/DispatchRecompute.py || { echo "Dispatch Recompute failed"; exit 1; }