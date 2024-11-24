#!/bin/bash

# Run the recompute script
python Scripts/WorkflowScripts/Recomputedata.py || { echo "Failed to run Recomputedata.sh"; exit 1; }

