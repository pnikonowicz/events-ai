FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

# data will be mounted in gcp
RUN rm -rf data
RUN rm -rf secrets

CMD [ "/usr/local/bin/python", "./web/fetch/main.py"]
