from scapy.all import sniff, IP, TCP
from scapy.contrib.mqtt import MQTT
from sender import EventSender
import numpy as np
#import pandas as pd

class MQTTSniffer:
    def __init__(self, iface, sport, dport):
        self.iface = iface
        self.dport = dport
        self.sport = sport

        log_array = []
        self.log_array = log_array
        

    def packet_callback(self, packet):
        if IP in packet and TCP in packet and (packet[TCP].sport == self.sport or packet[TCP].dport == self.dport) and MQTT in packet:
            srcAddr = packet[IP].src
            dstAddr = packet[IP].dst
            tcp_time = str(packet[TCP].time)
            mqtt_type = packet[MQTT].type
            mqtt_qos = packet[MQTT].QOS

            try:
                mqtt_length = packet[MQTT].length
                
                try:
                    mqtt_passwd = packet[MQTT].passwordflag
                except:
                    mqtt_passwd = 0

                self.siddhi_sender.send_event([str(tcp_time), str(srcAddr), str(dstAddr), mqtt_type, mqtt_length, mqtt_qos, mqtt_passwd])
            except AttributeError:
                None

    def start_sniffing(self, sender: EventSender):
        self.siddhi_sender = sender

        print(sender)
        print(f"Capturing packets from interface {self.iface} on port {self.dport}...")

        try:
            sniff(iface=self.iface, filter=f"tcp and port {self.dport}", prn=self.packet_callback)
        except KeyboardInterrupt:
            print("\nCapture interrupted.")
        finally:
            nparray = np.array(self.log_array)

