#!/bin/bash

# Update the repository to ensure it’s up to date
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "$BRANCH_NAME" || { echo "Failed to check out branch $BRANCH_NAME"; exit 1; }

# Run the configuration and data scripts
Scripts/WorkflowScripts/RunnerGitConfig.sh || { echo "Failed to configure Git"; exit 1; }
Scripts/WorkflowScripts/GetNewExperimentData.sh || { echo "Failed to get new experiment data"; exit 1; }
Scripts/WorkflowScripts/GetNewSimData.sh || { echo "Failed to get new simulation data"; exit 1; }
