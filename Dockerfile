# Use Kali Linux image
FROM kalilinux/kali-rolling

# Set working directory in the container
WORKDIR /app

# Copy everything from the scripts folder
COPY scripts/ ./scripts/

# Install required tools (Python and Bash)
RUN apt update && apt install -y python3 python3-pip bash

# Default command: open a bash shell
CMD ["/bin/bash"]
