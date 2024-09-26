# Use a base image with Git and necessary tools:
FROM ubuntu:latest

#Python:
RUN apt-get update && \
    apt-get install -y git python3 python3-pip python-is-python3
ENV GROMACS_VERSION=2024.3
ENV GITHUB_REPO_URL=https://github.com/MagnusSletten/Databank


# Install dependencies:
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    make \
    wget \
    curl \
    python3-pip \
    libfftw3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# Clone the repository at runtime using environment variables
RUN mkdir -p /app/Databank

CMD /bin/bash -c "\
    git clone https://$GH_TOKEN@github.com/MagnusSletten/Databank.git Databank && \
    cd Databank && \
    git fetch origin && git branch -r && \
    git fetch origin $TARGET_BRANCH && \
    git checkout $BRANCH_NAME && \
    chmod +x /app/Databank/.github/workflows/GetNewExperimentData.sh && \
    /app/Databank/.github/workflows/GetNewExperimentData.sh"

    