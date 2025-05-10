FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .

CMD [ "/usr/local/bin/python", "./web/fetch/main.py"]
