#!/bin/bash

# Update the repository to ensure it’s up to date
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "${BRANCH_NAME}" || { echo "Failed to check out branch ${BRANCH_NAME}"; exit 1; }
Scripts/WorkflowScripts/RunnerGitConfig.sh || { echo "Failed to configure git"; exit 1; }

# Run the recompute script
python Scripts/WorkflowScripts/Recomputedata.py --start-index "$START_INDEX" --end-index "$END_INDEX" --branch-name "$BRANCH_NAME" || { echo "Failed to run Recomputedata.py"; exit 1; }
