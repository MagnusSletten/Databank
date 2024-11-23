#!/bin/bash

# Pull the latest changes
git pull || { echo "git pull failed"; exit 1; }

# Push changes to the repository
git push https://x-access-token:$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git || { echo "git push failed"; exit 1; }
