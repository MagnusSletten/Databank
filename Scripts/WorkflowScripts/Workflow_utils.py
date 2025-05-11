from DatabankLib.core import initialize_databank 
import subprocess
import sys
import os


"""
Contains methods used for python scripts related to workflows. 
"""


#In order to get a consistent order of readme.yaml files we use sorting based on the ID.
def sorted_databank():
    systems = list(initialize_databank())
    systems.sort(key=lambda x: x['ID'])
    return systems

#Helper to run a shell command and exit on failure.
def run_command(command, error_message="Command failed", working_dir=None):
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_dir)
    except subprocess.CalledProcessError:
        print(error_message)
        sys.exit(1)

#Run a Python script using the current interpreter (sys.executable). Optional work directory can be applied.
def run_python_script(script_path, args=None, error_message="Python script failed", working_dir=None):
    if args is None:
        args = []
    try:
        subprocess.run(
            [sys.executable, script_path, *args],
            check=True,
            cwd=working_dir  # Set working directory if provided
        )
    except subprocess.CalledProcessError:
        print(error_message)
        sys.exit(1)


#TODO: Use package paths directly instead of this dictionary approach. 
def get_databank_paths(NMLDB_ROOT_PATH):
    Builddatabank_path = os.path.join(NMLDB_ROOT_PATH, "Scripts", "BuildDatabank")
    AddData_path = os.path.join(Builddatabank_path, "AddData.py")
    AnalyzeDatabank_path = os.path.join(NMLDB_ROOT_PATH, "Scripts", "AnalyzeDatabank")
    calcProperties_path = os.path.join(AnalyzeDatabank_path, "calcProperties.sh")
    searchDATABANK_path = os.path.join(Builddatabank_path, "searchDATABANK.py")
    QualityEvaluation_path = os.path.join(Builddatabank_path, "QualityEvaluation.py")
    makeRanking_path = os.path.join(Builddatabank_path, "makeRanking.py")

    return {
        "Builddatabank_path": Builddatabank_path,
        "AddData_path": AddData_path,
        "AnalyzeDatabank_path": AnalyzeDatabank_path,
        "calcProperties_path": calcProperties_path,
        "searchDATABANK_path": searchDATABANK_path,
        "QualityEvaluation_path": QualityEvaluation_path,
        "makeRanking_path": makeRanking_path
    }


def branch_exists(branch_name):
    """Return True if a local branch by that name already exists."""
    result = subprocess.run(
        f"git rev-parse --verify {branch_name}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def git_pull():
    run_command("git pull", "Failed to pull new files")

def git_commit(commit_message:str):
    run_command(f'git commit -m "{commit_message}"',"git commit failed")

def git_setup():
    GITHUB_USERNAME = "GitHub Actions Bot"
    GITHUB_EMAIL = "action@github.com"

    run_command(f'git config user.name "{GITHUB_USERNAME}"', "Failed to set Git username")
    run_command(f'git config user.email "{GITHUB_EMAIL}"', "Failed to set Git email")

def git_checkout_branch(branch_name):
    run_command(f'git checkout {branch_name}', f"Failed to check out branch {branch_name}")

def git_push(github_repository):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    run_command(
        f'git push https://x-access-token:{github_token}@github.com/{github_repository}.git',
        "git push failed"
    )

    
def get_branch_name():
    branch_name = os.getenv("BRANCH_NAME")
    if not branch_name:
        print("Branch name enviromental variable must be set")
        sys.exit(1) 
    return branch_name

def create_pull_request(branch_name, target_branch_name, github_actor):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("GITHUB_TOKEN not set.")
        sys.exit(1)

    run_command(
        f'gh pr create --head {branch_name} --base {target_branch_name} '
        f'--title "{github_actor}\'s New Data" '
        f'--body "This PR brings in new data from {github_actor}"',
        "Failed to create pull request"
    )

def create_branch_from_fork(pr_number, branch_name, github_repository):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    if branch_exists(branch_name):
        print(f"Error: branch '{branch_name}' already exists locally.")
        sys.exit(1)

    git_pull()
    run_command(
        f'git fetch origin pull/{pr_number}/head:{branch_name}',
        f"Failed to fetch PR #{pr_number}"
    )
    git_checkout_branch(branch_name)
    run_command(
        f'git push https://x-access-token:{github_token}@github.com/{github_repository} {branch_name}:{branch_name}',
        "Failed to push the branch"
    )

def create_branch(base_branch, new_branch_name, github_repository):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    git_checkout_branch(base_branch)
    git_pull()

    if branch_exists(new_branch_name):
        print(f"Error: branch '{new_branch_name}' already exists locally.")
        sys.exit(1)
    else:
        run_command(f'git checkout -b {new_branch_name}', f"Failed to create branch {new_branch_name}")

    print(f"Branch {new_branch_name} created based on {base_branch}.")
    run_command(
        f'git push https://x-access-token:{github_token}@github.com/{github_repository} {new_branch_name}:{new_branch_name}',
        "Failed to push the branch"
    )

def get_infofile_names_from_folder(folder_path):
    yaml_files = []
    try:
        file_names =  os.listdir(folder_path)
    except FileNotFoundError:
            print(f"Folder not found: {folder_path}")
            return None 
    for file in file_names:
        if file.lower().endswith(('.yaml', '.yml')):
            yaml_files.append(file)
    return yaml_files 
            
       
