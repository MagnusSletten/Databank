# Use an official Python runtime as a base image
FROM python:3.10-slim

# Install necessary dependencies and GitHub CLI
RUN apt-get update && \
    apt-get install -y curl git && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Add a non-root user 'runner'
RUN useradd -ms /bin/bash runner

# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Set up authentication and clone the repository before running the script
ENTRYPOINT ["bash", "-c", "\
  git clone https://x-access-token:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git && \
  cd $(basename $GITHUB_REPOSITORY) && \
  python Docker/DispatchRecompute.py"]
