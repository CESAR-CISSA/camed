#!/bin/bash

nmon -f -s 1 -c 140
sleep 140s;

RUN=1  # This value has to be indentic to the one set into cep.sh file
arquivo_nmon=$(ls -t *.nmon | head -n 1)

mv $arquivo_nmon $RUN.nmon


awk -F',' '/^CPU_ALL/ {print $1","$2","$3","$4","$5}' $RUN.nmon > $RUN.cpu_overall.csv
awk -F',' '/^MEM/ {print}' $RUN.nmon > $RUN.memory_data.csv
