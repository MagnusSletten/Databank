#!/bin/bash

# Push changes to the repository
git push https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git || { echo "git push failed"; exit 1; }
