FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ENV GIT_PYTHON_REFRESH=quiet
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10
ENV HOME="/home/vscode"

# Just
RUN wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | sudo tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null \
    && echo "deb [arch=all,$(dpkg --print-architecture) signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | sudo tee /etc/apt/sources.list.d/prebuilt-mpr.list \
    && apt-get update \
    && apt-get -y install just \
    && rm -rf /var/lib/apt/lists/*

# Prerequisites
RUN apt-get update \
    && apt-get -y install libsqlite3-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-venv \
        python3-pip \
        python${PYTHON_VERSION}-distutils \
        python3-apt \
        git && \
    rm -rf /var/lib/apt/lists/*
RUN pip install wheel --no-cache-dir --upgrade pip

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Terraform
RUN apt-get update \
    && apt-get install -y gnupg software-properties-common \
    && wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install terraform

# Postgresql client
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /home/vscode/.venv
ENV PATH="/home/vscode/.venv/bin:$PATH"

RUN mkdir /home/vscode/.ssh
RUN chmod -R 777 /home/vscode
RUN usermod -aG sudo vscode
