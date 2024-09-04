# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y \
    git \
    vim \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory (optional)
WORKDIR /workspace

# Clone the repository
RUN git clone https://github.com/hckr-cli/hckr.git

# Set the working directory to the cloned repo
WORKDIR /workspace/hckr

# Create a virtual environment and install hatch
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install hatch


# Set the default command to activate the virtual environment and open bash
CMD ["bash", "-c", "source venv/bin/activate && exec bash"]

