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
 && apt-get install -y --no-install-recommends \
	bash build-essential wget git vim \
	python3 \
	python3-pip python3-setuptools python3-six \
	python3-numpy python3-pandas \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir \
 && rm requirements.txt

# Install NLU
COPY install_nlu.sh .
RUN bash install_nlu.sh \
 && rm install_nlu.sh \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

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
LABEL maintainer.name = "Antonios Karteris"
LABEL maintainer.email = "akarteris@microlab.ntua.gr"
LABEL org.label-schema.build-date = $BUILD_DATE
LABEL org.label-schema.name = "Praetorian | WP6 T4 | Backend"
LABEL org.label-schema.description = "Praetorian H2020 Project | Work Package 6 : Response Coordination | Task 4 : Integration with Social Media | Backend Implementation"
LABEL org.label-schema.usage = "/docs/README.md"
LABEL org.label-schema.url = "https://praetorian-h2020.eu/"
LABEL org.label-schema.vcs-url = "https://github.com/Uphilld/praetorian-backend"
LABEL org.label-schema.vcs-ref = $GIT_SHA
LABEL org.label-schema.vendor = "Institute of Communication and Computer Systems (ICCS)"
LABEL org.label-schema.version = "RC"
LABEL org.label-schema.schema-version = "1.0"
LABEL org.label-schema.docker.cmd = "docker run -d --name praetorian_backend --log-driver local --network host -t uphilld/praetorian:backend"
LABEL org.label-schema.docker.cmd.devel = "docker run -it --name praetorian_backend_devel --log-driver local --network host -t uphilld/praetorian:backend"
LABEL org.label-schema.docker.cmd.help = "docker exec $CONTAINER /bin/bash /app/entrypoint.sh help"
