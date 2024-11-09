#!/bin/bash

# Source GROMACS environment to make gmx command available
source /usr/local/gromacs/bin/GMXRC || { echo "Failed to source GROMACS environment"; exit 1; }

# Update the repository to ensure it’s up to date
git pull || { echo "Failed to pull latest changes"; exit 1; }

# Check out the specified branch
git checkout "${BRANCH_NAME}" || { echo "Failed to check out branch ${BRANCH_NAME}"; exit 1; }
Scripts/DockerScripts/RunnerGitConfig.sh || { echo "Failed to configure git"; exit 1; }

# Run the recompute script
Scripts/DockerScripts/RecomputeSimdata.sh || { echo "Failed to run RecomputeSimdata.sh"; exit 1; }

