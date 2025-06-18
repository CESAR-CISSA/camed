#!/bin/bash

# Create a Docker network for MQTT
NETWORK_NAME="mqtt-net"

if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Creating Docker network..."
  docker network create "$NETWORK_NAME"
fi

# Create a directory for experiments if it doesn't exist
# This directory will store the nmon files and processed data
EXPERIMENTS_DIR="experiments"
mkdir -p $EXPERIMENTS_DIR

nmon -f -s 1 -c 140
sleep 140s;

RUN=1  # This value has to be indentic to the one set into cep.sh file
arquivo_nmon=$(ls -t *.nmon | head -n 1)

mv $arquivo_nmon $RUN.nmon

awk -F',' '/^CPU_ALL/ {print $1","$2","$3","$4","$5}' $RUN.nmon > $EXPERIMENTS_DIR/$RUN.cpu_overall.csv
awk -F',' '/^MEM/ {print}' $RUN.nmon > $EXPERIMENTS_DIR/$RUN.memory_data.csv