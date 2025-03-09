# Use the official Debian-based Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    procps \ 
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install conda
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh
ENV PATH="/opt/conda/bin:$PATH"

# Install additional packages directly
RUN pip install --no-cache-dir \
    pyspark \
    torch \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    polars \
    orjson \
    pyarrow \
    awswrangler \
    transformers \
    accelerate \
    duckdb \
    neo4j \
    s3fs \
    umap-learn \
    smart-open \
    onnxruntime \
    spacy \
    seqeval \
    gensim \
    numba \
    sqlalchemy \
    pytest \
    fsspec \
    "datasets>=2.0.0"

# Copy the rest of the application code
COPY . /app
WORKDIR /app

# Set the entrypoint
ENTRYPOINT ["sh", "-c"]
