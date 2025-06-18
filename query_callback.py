import csv
import os
import numpy as np
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
#import subprocess
import pandas as pd
import pickle

IP_ATTACKER = '172.18.0.20' # Change the IP accordaly in case you have change IPSEE code. 
FILE_OUTPUT_CSV = 'experiments/'+os.environ['RUN']+'.model_output.csv'
MODEL_FILE_PATH = 'model/model.pickle'

def load_model_and_scaler(path):

    with open(path, 'rb') as handle:
        pickle_obj = pickle.load(handle)

    return pickle_obj['model'], pickle_obj['scaler']


MODEL, SCALER = load_model_and_scaler('model/model.pickle')

def analisys_packet(data, model, ip_attacker, scaler, srcAddr):
        data = pd.DataFrame([data], columns=['mqtt_messagetype', 'mqtt_messagelength', 'mqtt_flag_passwd'])
        
        out_cep_scaled = scaler.transform(data)
        model_pred = model.predict(out_cep_scaled)
    
        model_pred = [1 if p == -1 else 0 for p in model_pred]

        if ip_attacker == srcAddr:
            is_attack = 1
        else:
            is_attack = 0

        return model_pred[0], is_attack


def write_output_analisys(filename, data):
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data) 
        except Exception as e:
            print(f"Error adding data to CSV file: {e}")


class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        if inEvents is not None:
            for event in inEvents:
                raw_data = event.getData()
                data = np.array(raw_data)

                timestamp   = data[0]
                srcAddr     = data[1]
                dstAddr     = data[2]
                mqtt_type   = data[3]
                mqtt_length = data[4]
                mqtt_passwd = data[5]
                ddos_attack = data[6]


                print(mqtt_type, mqtt_length, mqtt_passwd, srcAddr, IP_ATTACKER)
                
                model_pred, is_attack = analisys_packet(np.array([mqtt_type, mqtt_length, mqtt_passwd]), MODEL, IP_ATTACKER, SCALER, srcAddr) 
                output_data = np.append(data, [model_pred, is_attack], axis=0)
                write_output_analisys(FILE_OUTPUT_CSV, output_data)