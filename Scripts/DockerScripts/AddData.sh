#!/bin/bash

# Source GROMACS environment to ensure gmx command is available
source /usr/local/gromacs/bin/GMXRC || { echo "Failed to source GROMACS environment"; exit 1; }

# Update the repository to ensure it’s up to date
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "$BRANCH_NAME" || { echo "Failed to check out branch $BRANCH_NAME"; exit 1; }

# Run the configuration and data scripts
Scripts/DockerScripts/RunnerGitConfig.sh || { echo "Failed to configure Git"; exit 1; }
Scripts/DockerScripts/GetNewExperimentData.sh || { echo "Failed to get new experiment data"; exit 1; }
Scripts/DockerScripts/GetNewSimData.sh || { echo "Failed to get new simulation data"; exit 1; }
