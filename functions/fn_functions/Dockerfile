FROM  python:3.8-slim-buster

RUN apt-get update && apt-get install -y --no-install-recomends \
        build-essential \
        gcc \
        ca-certificates \
        git \
        curl \
        wget && \
    rm -rf /var/lib/apt/list/*

RUN pip install --no-cahe\
    request

ENV PYTHONDOWNTWRITEBYTECODE=1 \
    PYTHONONUBUFFERED=1 \
    PYTHONIOENCODING=UFT-8 \
    LANG=C.UFT-8 \
    LC_ALL=C.UFT-8

RUN mkdir -p /opt/ml/processing/output && \
    mkdir -p /opt/ml/processing/input && \
    mkdir -p /opt/ml/processing/code

ENV PATH="/opt/ml:${PATH}"

COPY download_file.py /opt/ml/processing/code/download_file.py

ENTRYPOINT ["python", "/opt/ml/processing/code/download_file.py"]