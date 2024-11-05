# Use a base image with Git and necessary tools:
FROM debian:bookworm-slim

ENV GROMACS_VERSION=2024.3

#Note: This still needs a enviromental variable with the repo url.

RUN apt-get update && apt-get install -y \
    bash \
    git \
    cmake \
    gcc \
    g++ \
    make \
    wget \
    curl \
    libfftw3-dev \
    python3 \
    python3-pip \
    llvm-dev \
    clang \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget https://ftp.gromacs.org/gromacs/gromacs-$GROMACS_VERSION.tar.gz && \
    tar xfz gromacs-$GROMACS_VERSION.tar.gz && \
    rm gromacs-$GROMACS_VERSION.tar.gz && \
    cd gromacs-$GROMACS_VERSION && \
    mkdir build && cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DGMX_GPU=OFF -DGMX_MPI=OFF && \
    make -j$(nproc) && \
    make install


RUN echo "source /usr/local/gromacs/bin/GMXRC" >> /etc/profile


# Install Python packages with --break-system-packages flag to avoid externally managed environment errors:
RUN pip3 install --break-system-packages pytest tqdm pyyaml pandas buildh Cython


WORKDIR /app 
# Clone the MDAnalysis repository
RUN git clone --branch develop https://github.com/MDAnalysis/mdanalysis.git && \
    cd mdanalysis/package && \
    python3 setup.py install && \
    cd ../.. && rm -rf mdanalysis

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
    git clone https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git Databank && \
    cd Databank && \
    git fetch origin && git branch -r && \
    git checkout $BRANCH_NAME && \
    Scripts/DockerScripts/RecomputeSimdata.sh"
