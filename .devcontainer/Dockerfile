FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install nvm
ENV BASH_ENV=/root/.bash_env
RUN touch "${BASH_ENV}"
RUN echo '. "${BASH_ENV}"' >> ~/.bashrc
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | PROFILE="${BASH_ENV}" bash

RUN echo node > .nvmrc
RUN nvm install --lts && nvm --version

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# RUN rm -rf data

CMD [ "/usr/local/bin/python", "./web/server/main.py"]