ARG UBUNTU_VERSION=20.04
ARG TESSERACT_VERSION=5.3.4

FROM jitesoft/tesseract-ocr
RUN train-lang eng --fast

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER root

# Install Python, pip, and Ghostscript
RUN apt-get update && \
    apt-get install -y python3 python3-pip ghostscript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copy your Python script into the container
COPY src /app/src
COPY test_data /app/test_data 
COPY run.py /app/run.py

# Set a working directory
WORKDIR /app

RUN chown -R tesseract:tesseract /app
USER tesseract

ENTRYPOINT ["gunicorn"]
