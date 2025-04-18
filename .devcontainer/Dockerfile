FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# ENV NVM_DIR=/root/.nvm

# Use bash for the shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Create a script file sourced by both interactive and non-interactive bash shells
ENV BASH_ENV /root/.bash_env
RUN touch "${BASH_ENV}"
RUN echo '. "${BASH_ENV}"' >> ~/.bashrc

RUN apt update -y && apt install curl -y \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | PROFILE="${BASH_ENV}" bash

RUN echo node > .nvmrc
RUN nvm install --lts && nvm --version

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "echo", "welcome to events-ai dev contianer"]
# ENTRYPOINT sleep infinity