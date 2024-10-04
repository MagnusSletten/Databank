FROM python:3.10-slim


RUN apt-get update && \
    apt-get install -y curl git && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
# Add a non-root user 'runner'
RUN useradd -ms /bin/bash runner

# Copy the Python script into the container
COPY DispatchRecompute.py .
    
# Change ownership of the /app directory to 'runner'
RUN chown -R runner:runner /app

# Switch to 'runner' user
USER runner

# Set up authentication before running the script
ENTRYPOINT ["bash", "-c", "\
  echo \"$GITHUB_TOKEN\" | gh auth login --with-token && \
  python DispatchRecompute.py"]