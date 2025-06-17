# CAMED - Contextual Anomaly Mitigation for Event-Driven Systems

CAMED is a tool designed to identify anomalous behavior attacks within the MQTT protocol by integrating Complex Event Processing (CEP) with machine learning–driven anomaly detection.

## Project structure

```
camed/
├── data/
│   └── eventos.csv                         # 
├── model/
│   └── model.pickle                        # The machine learn model pickle file
├── app.py                                  #
├── ipsee.py                                # Scapy sniffer
├── main.py                                 #
├── manager.py                              #
├── mqtt_stream.py                          #
├── net_helper.py                           # Helper to network interfaces selection
├── query_callback.py                       #
├── sender.py                               #
├── siddhi_query.py                         #
├── stream_schema.py                        #
├── cep.sh                                  # 
├── start_nmon.sh                           # Bash script to run nmon and collect the system performance statistics
├── requirements.txt                        # Required python libraries
├── README.md                               # This file
```

## Installation
### Dependences
- nmon
- Python 3.6+
- PySiddhi 5.1.0
- Additional dependencies listed in requirements.txt

### How to install

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt

#### Disclamer: Ensure you have Java installed (required by PySiddhi)

## How to execute
### Requirements:
You must have a docker network running and configured in the project's dockerfile (We define the creation of the network in the nmon script for redundancy purposes)
    
### Running

    $ sudo su
    $ source venv/bin/activate
    $ ./start_nmon.sh

##### Disclamer: Run nmon script in exclusive terminal with root privileges

#### 1. Execte as a python script:
    $ export RUN=1                          # Change this value with your desired RUN value
    $ export SIDDHISDK_HOME=/home/user/Sidhi/siddhi-sdk-5.1.2 # Change your values acordatily
    $ export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    $ python3 camed.py

#### 2. Execte as a bash script:
    $ ./camed.sh