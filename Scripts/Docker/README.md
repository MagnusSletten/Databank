# Information about Docker images for NMRLipids project

## Running the core image locally
The core image features software needed to work with the NMRLipid Databank. 

To use it locally you can run:

```
docker pull nmrlipids/core
```
Then you can run it in interactive mode:

```
docker run -it nmrlipids/core
```
From here you can work with the repository directly through normal git commands, for instance:

```
git clone https://github.com/NMRLipids/Databank
```
To exit interactive mode simply type:

```
exit
```
## Information about the core dockerfile
It uses a two stage process: a build stage where Gromacs is built then a final stage which just contains dependencies that are relevant for development. Gromacs is copied from the build stage into the final stage. This setup reduces the overall size of the image. 

MDAnalysis is installed with the latest development version directly through Git.

Gromacs version can be specified at the top of the dockerfile. There's also an option for the Gromacs version to be specified through an enviromental variable, but this is more relevant for CICD-purposes.

## How to build locally
To build the image locally you can run the following command **from root of the repository**:

```
docker build -f Scripts/Docker/core -t nmrlipids/core .
```
(Note that this process takes quite a bit of time)

It copies the development version of the requirements-file from the repository which is why the the above command needs be run from root of repository. 


