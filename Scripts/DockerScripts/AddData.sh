#!/bin/bash

# Update the repository to ensure it’s up to date
git pull  || { echo "Failed to pull latest changes"; exit 1; }
Scripts/DockerScripts/RunnerGitConfig.sh &&
Scripts/DockerScripts/GetNewExperimentData.sh &&
Scripts/DockerScripts/GetNewSimData.sh
