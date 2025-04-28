from WorkflowScripts.Workflow_utils import *

import os
import sys

def main():
    #Sets up git:
    git_setup()
    #Updates starting branch:
    git_pull()
    branch_name = os.getenv("BRANCH_NAME")
    #Checks out branch
    git_checkout_branch(branch_name)
    #Updates the checked out branch
    git_pull()
    #Running scripts:
    run_command("Scripts/WorkflowScripts/GetNewExperimentData.sh", "Experiment data script failed")
    run_command("Scripts/WorkflowScripts/GetNewSimData.sh","Simulation data script failed")

if __name__ == "__main__":
    main()