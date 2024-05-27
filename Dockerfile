ARG UBUNTU_VERSION=20.04
ARG TESSERACT_VERSION=5.3.4

FROM jitesoft/tesseract-ocr

USER root

# Install Python, pip, and Ghostscript
RUN apt-get update && \
    apt-get install -y python3 python3-pip ghostscript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy your Python script into the container
COPY src /app/src
COPY test_data /app/test_data 
COPY requirements.txt /app/requirements.txt

# Set a working directory
WORKDIR /app

# Install Python libraries
RUN pip3 install -r requirements.txt

RUN chown -R tesseract:tesseract /app
USER tesseract

# Check permissions and user details
RUN ls -l /app && whoami

# Run your training script
RUN train-lang eng --fast

ENTRYPOINT ["python3"]
# The default command or entrypoint to run the Python script
CMD ["src/minimum_viable_ocr.py"]
