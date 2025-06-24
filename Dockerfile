FROM debian:bookworm-slim AS builder

# Build args
ARG GROMACS_VERSION=2025.2
ARG MAKE_JOBS
ENV GROMACS_VERSION=${GROMACS_VERSION}

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      bash wget python3.11 python3-pip bzip2 ca-certificates build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install CMake via pip for building GROMACS
RUN pip3 install --no-cache-dir cmake --break-system-packages

# Download & build GROMACS
RUN wget https://ftp.gromacs.org/gromacs/gromacs-${GROMACS_VERSION}.tar.gz && \
    tar xzf gromacs-${GROMACS_VERSION}.tar.gz && \
    rm gromacs-${GROMACS_VERSION}.tar.gz && \
    cd gromacs-${GROMACS_VERSION} && mkdir build && cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON && \
    make -j${MAKE_JOBS:-$(nproc)} && \
    make check -j${MAKE_JOBS:-$(nproc)} && \
    make install && \
    cd / && rm -rf gromacs-${GROMACS_VERSION}

# Install Miniconda and create 'databank' env with requirements
ARG MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
RUN wget --quiet ${MINICONDA_URL} -O /tmp/conda.sh && \
    bash /tmp/conda.sh -b -p /opt/conda && \
    rm /tmp/conda.sh && \
    /opt/conda/bin/conda clean --all --yes
ENV PATH="/opt/conda/bin:${PATH}"

# Copy requirements and install into Conda env
COPY Scripts/DatabankLib/requirements-dev.txt requirements-dev.txt
RUN conda create -n databank python=3.11 --yes && \
    conda run -n databank pip install --no-cache-dir -r requirements-dev.txt && \
    conda clean --all --yes && \
    rm requirements-dev.txt

# Final stage: minimal runtime with GROMACS + Conda env
FROM debian:bookworm-slim AS final

# Copy GROMACS and Conda env from builder
COPY --from=builder /usr/local/gromacs /usr/local/gromacs
COPY --from=builder /opt/conda /opt/conda

# Install bash, git, CA certificates for HTTPS cloning, OpenMP runtime for GROMACS, and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      bash \
      git \
      ca-certificates \
      libgomp1 \
      python3 \
      python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Expose Conda executable, Conda env, and GROMACS in PATH
ENV PATH="/opt/conda/bin:/opt/conda/envs/databank/bin:/usr/local/gromacs/bin:${PATH}"

# Create and switch to non-root runner user
RUN useradd -m -s /bin/bash runner
USER runner

# Enable Conda in interactive shells
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/runner/.bashrc && \
    echo "conda activate databank" >> /home/runner/.bashrc


# Set working directory and default command
WORKDIR /workspace
 