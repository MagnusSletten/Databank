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

# Download and unzip gromacs:
RUN wget https://ftp.gromacs.org/gromacs/gromacs-$GROMACS_VERSION.tar.gz && \
tar xfz gromacs-$GROMACS_VERSION.tar.gz && \
rm gromacs-$GROMACS_VERSION.tar.gz

# Trying without features we don't need:
RUN cd gromacs-$GROMACS_VERSION && \
    mkdir build && cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DGMX_GPU=OFF -DGMX_MPI=OFF && \
    make -j$(nproc) && \
    make install

    # Add a non-root user 'runner'
RUN useradd -m -s /bin/bash runner

# Set working directory
WORKDIR /app

# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Clone the repository at runtime using environment variables
RUN mkdir -p /app/Databank

CMD /bin/bash -c "source /usr/local/gromacs/bin/GMXRC && \
    git clone https://$GH_TOKEN@github.com/MagnusSletten/Databank.git Databank && \
    cd Databank && \
    git fetch origin && git branch -r && \
    git checkout $BRANCH_NAME && \
    chmod +x /app/Databank/.github/workflows/RecomputeSimdata.sh && \
    /app/Databank/.github/workflows/RecomputeSimdata.sh"
