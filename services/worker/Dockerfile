ARG UBUNTU_VERSION=20.04
ARG TESSERACT_VERSION=5.3.4

FROM jitesoft/tesseract-ocr
RUN train-lang eng --fast

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER root

# Install Python, pip, and Ghostscript
RUN apt-get update && \
    apt-get install -y python3 python3-pip ghostscript poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY requirements.txt /home/app/requirements.txt
RUN pip3 install -r /home/app/requirements.txt

# Copy your Python script into the container
COPY . /home/app/
RUN mkdir -p /home/app/pdf_out


# Set a working directory
WORKDIR /home/app

RUN chown -R tesseract:tesseract /home/app
RUN chown -R tesseract:tesseract /home/app/pdf_out

USER tesseract

ENTRYPOINT ["celery"]
