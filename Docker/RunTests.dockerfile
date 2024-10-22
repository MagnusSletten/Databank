#Starting from ubuntu
FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"] 

# Setting environment variables
ENV GROMACS_VERSION=2024.3
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, some of these might not be needed: 
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    make \
    wget \
    curl \
    python3-pip \
    libperl4-corelibs-perl \
    libfftw3-dev \
    git \
    build-essential \
    perl \
    libfile-copy-recursive-perl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and unpack the latest GROMACS:
RUN wget https://ftp.gromacs.org/gromacs/gromacs-$GROMACS_VERSION.tar.gz && \
    tar xfz gromacs-$GROMACS_VERSION.tar.gz && \
    rm gromacs-$GROMACS_VERSION.tar.gz

# Build and install GROMACS per instructions from the official guide:
RUN cd gromacs-$GROMACS_VERSION && \
    mkdir build && cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON && \
    make && \
    make check && \  
    make install && \
    source /usr/local/gromacs/bin/GMXRC


RUN pip3 install pytest MDAnalysis MDAnalysisTests tqdm pyyaml pandas buildh
WORKDIR /app

# Add a non-root user 'runner'
RUN useradd -m -s /bin/bash runner

# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Clone the repository at runtime using environment variables
RUN mkdir -p /app/Databank

# Set the default command to run pytest after sourcing GROMACS
CMD ["/bin/bash", "-c", "git clone --branch $BRANCH_NAME https://github.com/MagnusSletten/Databank.git /app/Databank && \
cd /app/Databank/Scripts/tests/ && \
source /usr/local/gromacs/bin/GMXRC && \
pytest -vs"]
