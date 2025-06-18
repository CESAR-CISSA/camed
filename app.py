from PySiddhi.core.SiddhiManager import SiddhiManager
from mqtt_stream import MQTTStream, SiddhiType
from net_helper import NetworkInterfaceManager
from ipsee import MQTTSniffer
from query_callback import QueryCallbackImpl
from siddhi_query import SiddhiQuery
from sender import EventSender
from time import sleep
import asyncio
import subprocess

async def main():
    # Instantiate the MQTT stream
    mqtt_stream = MQTTStream("cseEventStream")
    mqtt_stream.add_mqtt_attribute("sniff_ts", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("srcAddr", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("dstAddr", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("mqtt_messagetype", SiddhiType.INT)
    mqtt_stream.add_mqtt_attribute("mqtt_messagelength", SiddhiType.LONG)
    mqtt_stream.add_mqtt_attribute("mqtt_flag_qos", SiddhiType.INT)
    mqtt_stream.add_mqtt_attribute("mqtt_flag_passwd", SiddhiType.INT)

    # Define the Siddhi query
    query = SiddhiQuery(
        name="query1",
        query_string="""
        define stream cseEventStream (sniff_ts string, srcAddr string, dstAddr string, mqtt_messagetype int, mqtt_messagelength long, mqtt_flag_qos int, mqtt_flag_passwd int);          
            @info(name = 'query1')
                from cseEventStream#window.time(500 milliseconds)
                select sniff_ts, srcAddr, dstAddr, mqtt_messagetype, mqtt_messagelength, mqtt_flag_passwd, count() as eventCount
                group by srcAddr
                having eventCount >= 50
                insert into TempWindow;
        """
    )

    siddhi_manager = SiddhiManager()
    siddhi_app = str(mqtt_stream) + " " + str(query)

    siddhi_runtime = siddhi_manager.createSiddhiAppRuntime(siddhi_app)

    # Sets the column names in the order used in the stream
    column_names = mqtt_stream.get_attribute_names()

    # Add callback with real names
    # siddhi_runtime.addCallback(query.name, QueryCallbackImpl(column_names=column_names))
    # siddhi_runtime.addCallback(query.name, QueryCallbackImpl())
    siddhi_runtime.addCallback('query1', QueryCallbackImpl())

    input_handler = siddhi_runtime.getInputHandler(mqtt_stream.stream_name)


    sender = EventSender(input_handler, mqtt_stream)
    siddhi_runtime.start()

    manager = NetworkInterfaceManager()
    #selected_interface = manager.choose_interface_cli()


    #print(selected_interface)
    command = "docker network ls | grep mqtt | awk '{print \"br-\"$1}'"
    selected_interface = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    selected_interface = selected_interface.stdout.strip()


    iface = selected_interface
    sport = 1883
    dport = 1883

    sniffer = MQTTSniffer(iface, sport, dport) 
    sniffer.start_sniffing(sender)

    sleep(5)
    siddhi_manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
