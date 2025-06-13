import csv
from PySiddhi.DataTypes.LongType import LongType
import asyncio

from mqtt_stream import MQTTStream

class EventSender:
    def __init__(self, input_handler, stream: MQTTStream):
        self.input_handler = input_handler
        self.stream = stream

    def _get_attribute_order(self):
        return [name for name in self.stream.get_attributes().keys()]

    def _format_event(self, attribute_order, values):
        """Formats an event according to defined types."""
        event = []
        for idx, attr_name in enumerate(attribute_order):
            tipo = self.stream.get_attributes()[attr_name]
            val = values[idx]
            if tipo == "long":
                if val == '':
                    continue
                else:
                    event.append(LongType(int(float(val))))
            else:
                event.append(val)
        return event

    def send_event(self, values: list):
        """
        Sends a single event to Siddhi from a list of values.
        
        Parameters:
            values (list): List of values in the order of the stream attributes.
        """
        attribute_order = self._get_attribute_order()
        if len(values) != len(attribute_order):
            raise ValueError(f"Number of values ({len(values)}) does not match number of attributes ({len(attribute_order)}).")

        event = self._format_event(attribute_order, values)
        self.input_handler.send(event)

    def send_event_from_dict(self, data: dict):
        """
        Converts a dictionary of attributes into an ordered list and dispatches the event.
        """
        attribute_order = self._get_attribute_order()
        try:
            values = [data[attr] for attr in attribute_order]
        except KeyError as e:
            raise ValueError(f"Missing field in dictionary: {e.args[0]}")
        self.send_event(values)

    async def send_event_from_csv(self, csv_path: str):
        """
        Reads CSV line by line asynchronously and sends events to Siddhi.
        """
        attribute_order = self._get_attribute_order()

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                values = [row[field] for field in attribute_order]
                event = self._format_event(attribute_order, values)
                self.input_handler.send(event)
                await asyncio.sleep(0)  # Yield for the event loop

    def _count_records(self, csv_path: str) -> int:
        """Counts the number of records in the CSV, ignoring the header."""
        with open(csv_path, newline='') as csvfile:
            return sum(1 for _ in csvfile) - 1
