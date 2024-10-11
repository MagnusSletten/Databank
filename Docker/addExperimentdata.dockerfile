# Use a base image with Git and necessary tools:
FROM ubuntu:latest

# Python and system dependencies:
RUN apt-get update && \
    apt-get install -y git python3 python3-pip python-is-python3

ENV GROMACS_VERSION=2024.3
ENV GITHUB_REPO_URL=https://github.com/MagnusSletten/Databank

# Install system dependencies:
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    make \
    wget \
    curl \
    libfftw3-dev \
    build-essential \
    python3-yaml \
    && apt-get clean && rm -rf /var/lib/apt/lists/*  
#double check last line 

# Add a non-root user 'runner'
RUN useradd -ms /bin/bash runner

# Set working directory
WORKDIR /app

# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Clone the repository at runtime using environment variables
#Check depth 
CMD /bin/bash -c "\
    git clone https://$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git  --branch=$BRANCH_NAME Databank && \  
    cd Databank && \
    git fetch origin && git branch -r && \
    chmod +x /app/Databank/.github/workflows/GetNewExperimentData.sh && \
    /app/Databank/.github/workflows/GetNewExperimentData.sh"

