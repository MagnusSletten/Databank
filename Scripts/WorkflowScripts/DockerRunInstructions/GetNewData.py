from WorkflowScripts.Workflow_utils import *
from DatabankLib import NMLDB_SIMU_PATH
from DatabankLib import NMLDB_ROOT_PATH
from WorkflowScripts import ProcessInfoFile 
import os
import sys

def main():
    ProcessInfoFile_path = os.path.abspath(ProcessInfoFile.__file__)
    data_folder_path = os.path.join(NMLDB_ROOT_PATH,"UserData")
    
    #Sets up git:
    git_setup()
    #Updates starting branch:
    git_pull()
    branch_name = get_branch_name()
    #Checks out branch
    git_checkout_branch(branch_name)
    #Updates the checked out branch
    git_pull()
    #Running scripts:
    run_python_script(ProcessInfoFile_path,["--info_file_folder",data_folder_path])



if __name__ == "__main__":
    main()