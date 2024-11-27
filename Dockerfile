FROM python:3.8-slim

# using root user
USER root:root

#install dependencies 
RUN apt-get update \
&& apt-get install zip unzip -y

#install gcloud
RUN apt-get install apt-transport-https ca-certificates gnupg -y \
&& echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
| tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
| apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
&& apt-get update && apt-get install google-cloud-cli -y

#install additional packages
RUN pip3 install --upgrade pip \
&& pip3 install apache-beam[gcp] \
&& pip3 install google-cloud-storage \
&& pip3 install google-cloud-bigquery

#define workspace
COPY ./certificacao-GCP/ /opt/python/
WORKDIR /opt/python/