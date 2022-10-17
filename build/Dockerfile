#!/usr/bin/env python3
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Image recipe

# Pull base tf image
FROM tensorflow/tensorflow:2.9.1-gpu

# Set working directory
WORKDIR /app

# Install packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends -q \
	build-essential \
	bash git vim wget \
	openjdk-8-jdk-headless \
	python3 \
	python3-pip python3-setuptools python3-six \
	python3-numpy python3-pandas \
 && apt-get autoremove -y -q \
 && apt-get clean -y -q \
 && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt .
RUN pip3 install -q --no-cache-dir -r requirements.txt \
 && rm requirements.txt

# Set enviroment variables
ENV SPARK_HOME="/app/spark-3.0.2-bin-hadoop2.7"
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"

# Install NLU prerequisites
RUN wget -nv "https://archive.apache.org/dist/spark/spark-3.0.2/spark-3.0.2-bin-hadoop2.7.tgz" \
 && tar -xf spark-3.0.2-bin-hadoop2.7.tgz \
 && rm -rf spark-3.0.2-bin-hadoop2.7.tgz

# Install NLU
RUN pip3 install --upgrade -q --no-cache-dir pyspark==3.0.3 spark-nlp==3.4.0 findspark nlu==3.4.1rc5

# Copy ML models
COPY models /app/models

# Copy the credentials
COPY credentials.env /app

# Copy the entrypoint
COPY entrypoint.sh /app

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Set labels according to Label Schema Convention
# http://label-schema.org/rc1/
ARG BUILD_DATE
ARG GIT_SHA
LABEL maintainer "Antonios Karteris <akarteris@microlab.ntua.gr>"
LABEL org.label-schema.build-date $BUILD_DATE
LABEL org.label-schema.name "Praetorian | WP6 T4 | Backend"
LABEL org.label-schema.description "Praetorian H2020 Project | Work Package 6 : Response Coordination | Task 4 : Integration with Social Media | Backend Implementation"
LABEL org.label-schema.usage "/docs/README.md"
LABEL org.label-schema.url "https://praetorian-h2020.eu/"
LABEL org.label-schema.vcs-url "https://github.com/Uphilld/praetorian-backend"
LABEL org.label-schema.vcs-ref $GIT_SHA
LABEL org.label-schema.vendor "Institute of Communication and Computer Systems (ICCS)"
LABEL org.label-schema.version "RC"
LABEL org.label-schema.schema-version "1.0"
LABEL org.label-schema.docker.cmd "docker run -d --name praetorian_backend --log-driver local --network host -t uphilld/praetorian:backend"
LABEL org.label-schema.docker.cmd.devel "docker run -it --name praetorian_backend_devel --log-driver local --network host -t uphilld/praetorian:backend"
LABEL org.label-schema.docker.cmd.help "docker exec $CONTAINER /bin/bash /app/entrypoint.sh help"
