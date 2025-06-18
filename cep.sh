#!/bin/bash

# This variable is responsible to create a file with an specific RUN value.
export RUN=1

export SIDDHISDK_HOME=/home/phgl/siddhi-sdk-5.1.2 # Change your values acordatily
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

sleep 10s; timeout 130s python3 app.py
