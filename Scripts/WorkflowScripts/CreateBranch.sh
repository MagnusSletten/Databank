#!/bin/bash

#Creates a new branch identical to a given base branch within the repository:

# Ensure base branch is up-to-date and exists locally
git checkout ${BASE_BRANCH} || { echo "Base branch ${BASE_BRANCH} not found"; exit 1; }
git pull origin ${BASE_BRANCH} || { echo "Failed to pull latest ${BASE_BRANCH}"; exit 1; }

# Create new branch from the base branch
git checkout -b ${BRANCH_NAME} || { echo "Failed to create branch ${BRANCH_NAME}"; exit 1; }
echo "Branch ${BRANCH_NAME} created based on ${BASE_BRANCH}."
# Push the new branch to the main repository
git push https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY} ${BRANCH_NAME}:${BRANCH_NAME} || { echo "Failed to push the branch"; exit 1; }