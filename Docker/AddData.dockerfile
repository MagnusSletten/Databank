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


RUN pip3 install --break-system-packages pytest tqdm pyyaml pandas buildh Cython

WORKDIR /app 
# Clone the MDAnalysis repository
RUN git clone --branch develop https://github.com/MDAnalysis/mdanalysis.git && \
    cd mdanalysis/package && \
    python3 setup.py install && \
    cd ../.. && rm -rf mdanalysis


# Add a non-root user 'runner'
RUN useradd -m -s /bin/bash runner

# Create a symbolic link for python -> python3
RUN ln -s /usr/bin/python3 /usr/bin/python


WORKDIR /app


RUN chown -R runner:runner /app

USER runner


# Command to clone the repo and run both experiment and simdata scripts
CMD /bin/bash -c "source /usr/local/gromacs/bin/GMXRC && \
    git clone https://$GITHUB_TOKEN@github.com/MagnusSletten/Databank.git --branch=$BRANCH_NAME Databank && \
    cd Databank && \
    git fetch origin && git branch -r && \
    Scripts/DockerScripts/RunnerGitConfig.sh && \
    Scripts/DockerScripts/GetNewExperimentData.sh && \
    Scripts/DockerScripts/GetNewSimData.sh"