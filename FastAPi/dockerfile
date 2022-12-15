FROM continuumio/miniconda3 AS build
RUN apt-get update
# Installing git and SSH in case required by conda
RUN apt-get install -y git openssh-client openssh-server ca-certificates
RUN git config --global http.sslVerify false
# Authorize SSH Host
RUN mkdir -p /home/appuser/.ssh
RUN chmod 0700 /home/appuser/.ssh
RUN ssh-keyscan github.com > /home/appuser/.ssh/id_github
# Updating conda
RUN conda update -n base -c defaults conda
WORKDIR /app
COPY . .
# Creating the environment
RUN --mount=type=ssh,id=id_github conda env create -f environment.yml