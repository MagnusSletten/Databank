# Info about how to use Github Actions

## Adding data via a pull request from fork

The main github action here is: NewDataPipeline.yml and it does two things:


The new data pipeline relies on this workflow file to handle information from an incoming branch in a fork. It will first create a new branch and then open a pull request with the following setup:
    
1. First, create a new branch on this repository identical to the incoming branch from fork
2. Then, open a pull request with the following setup:
       
    * The base of the new pull request will match the branch that the fork's pull request is targeting.
    * Example: If the fork is targeting the `main` branch with added files, this workflow creates a new branch in this repository and opens a pull request to the `main` branch of this repository.

3. Then the AddData.yml workflow will be started with the info about relevant branches. This will go through the steps for adding experiment data first then the steps for adding simulation data. If no experiment data is present then those steps will be skipped. This design is simple and less error prone than more advanced designs. The scripts for adding experiment data and simulation data is in Scripts/DockerScripts. 
The automated steps are described here: (insert link here). 




## Recomputing Data

You can initiate recomputes of simulation data using the workflow file: `RecomputeDatabank.yml`. The following options allow you to specify which files to recompute and control the distribution of the workload:

- **Specify File Range**: Use the starting and ending index to define which info files to recompute.
  - **All Files**: Set the starting index to `0` and the ending index to `-1` (negative one) to recompute all files.
  
- **Set Number of Runners**: Define the number of runners to split the recompute job. Each runner will process its portion of the files and commit the results to a specified branch.
  - For example, if there are 100 files and you specify 5 runners, each runner will handle 20 files.

This setup enables parallel processing, with each runner working on a distinct subset of files.


## Docker Image Builder Workflow

This workflow file, `BuildDockerImages.yml`, allows you to rebuild and push specific Docker images to Docker Hub. The purpose is to make rebuilding the dockerimage easy when that is needed, for instance with major updates to dependencies, like MDanalsysis. 
#### Triggering the Workflow

The workflow can be triggered manually with the `workflow_dispatch` event, allowing you to specify which Docker image to rebuild.

#### Inputs

- `docker_image_name` (required): The name of the Docker image you want to rebuild and push. This should match the image names in the repository (e.g., `add_data`, `recompute_instance`, `tests`).

#### Steps in the Workflow

1. **Log in to Docker Hub**:
   - Uses Docker Hub credentials (stored as `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets) to authenticate before building and pushing images.

2. **Build Docker Image**:
   - Builds the specified Docker image based on the input provided. The image is tagged using the `nmrlipids/` prefix and the `latest` tag by default.

3. **Push Docker Image to Docker Hub**:
   - Pushes the tagged image to Docker Hub under the `nmrlipids/` namespace.

#### Example Usage

To manually trigger the workflow, go to the **Actions** tab in your GitHub repository, select `BuildDockerImages`, and click **Run workflow**. Enter the `docker_image_name` (e.g., `add_data`) to specify which image to rebuild.

#### Repository Structure

Dockerfiles are located in the `Docker` folder at the root of the repository, with names matching the Docker image names:
- `add_data` for the `nmrlipids/add_data` Docker image
- `recompute_instance` for the `nmrlipids/recompute_instance` Docker image
- `tests` for the `nmrlipids/tests` Docker image
