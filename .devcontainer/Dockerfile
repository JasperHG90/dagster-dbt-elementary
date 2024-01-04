FROM mcr.microsoft.com/devcontainers/python:3.10
ENV PYTHONUNBUFFERED 1
ENV PIPX_HOME="/home/vscode/.pipx"

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y gdal-bin libgdal-dev g++ pipx

RUN wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | sudo tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null \
    && echo "deb [arch=all,$(dpkg --print-architecture) signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | sudo tee /etc/apt/sources.list.d/prebuilt-mpr.list \
    && apt-get update \
    && apt-get -y install just \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pipx install poetry

ENV PATH="/home/vscode/.local/bin:$PATH"
RUN mkdir /home/vscode/.ssh
RUN chmod -R 777 /home/vscode
RUN usermod -aG sudo vscode
