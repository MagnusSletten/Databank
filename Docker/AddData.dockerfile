# Use a lightweight Debian-based base image
FROM debian:bookworm-slim

# Set environment variables
ENV GROMACS_VERSION=2024.3
ENV GITHUB_REPO_URL=https://github.com/MagnusSletten/Databank

# Install necessary dependencies
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

# Download and build GROMACS without GPU or MPI
RUN wget https://ftp.gromacs.org/gromacs/gromacs-$GROMACS_VERSION.tar.gz && \
    tar xfz gromacs-$GROMACS_VERSION.tar.gz && \
    rm gromacs-$GROMACS_VERSION.tar.gz && \
    cd gromacs-$GROMACS_VERSION && \
    mkdir build && cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DGMX_GPU=OFF -DGMX_MPI=OFF && \
    make -j$(nproc) && \
    make install

# Make GROMACS available globally
RUN echo "source /usr/local/gromacs/bin/GMXRC" >> /etc/profile

# Install Python packages with the --break-system-packages flag to avoid externally managed environment errors
RUN pip3 install --break-system-packages pytest MDAnalysis MDAnalysisTests tqdm pyyaml pandas buildh

# Add a non-root user 'runner'
RUN useradd -m -s /bin/bash runner

# Set working directory
WORKDIR /app

# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Command to clone the repo and run both experiment and simdata scripts
CMD /bin/bash -c "source /usr/local/gromacs/bin/GMXRC && \
    git clone https://$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git --branch=$BRANCH_NAME Databank && \
    cd Databank && \
    git fetch origin && git branch -r && \
    chmod +x /app/Databank/.github/workflows/GetNewExperimentData.sh && \
    chmod +x /app/Databank/.github/workflows/GetNewSimData.sh && \
    /app/Databank/.github/workflows/GetNewExperimentData.sh && \
    /app/Databank/.github/workflows/GetNewSimData.sh"
