from enum import Enum

from stream_schema import StreamSchema

class SiddhiType(str, Enum):
    STRING = "string"
    INT = "int"
    LONG = "long"
    DOUBLE = "double"
    FLOAT = "float"
    BOOL = "bool"


class MQTTStream(StreamSchema):
    def __init__(self, stream_name: str):
        self.stream_name = stream_name
        self.__attribute_types = {}  # Private dictionary

    def add_mqtt_attribute(self, attr_name: str, attr_type: str):
        """
        Adds a new MQTT attribute with type validation.
        """
      
        attr_type = attr_type.lower()
        if attr_type not in SiddhiType._value2member_map_:
            raise ValueError(f"Tipo '{attr_type}' inválido. Tipos válidos: {[t.value for t in SiddhiType]}")

        setattr(self, attr_name, None)
        self.__attribute_types[attr_name] = attr_type

    def defineStreamString(self) -> str:
        stream_def_parts = []
        for attr_name in self.__dict__:
            if attr_name.startswith('mqtt_'):
                tipo = self.__attribute_types.get(attr_name, 'string')
                stream_def_parts.append(f"{attr_name} {tipo}")
        atributos_str = ", ".join(stream_def_parts)
        return f"define stream {self.stream_name}({atributos_str});"
        
    def __str__(self):
        stream_def_parts = []
        for attr_name in self.__attribute_types:
            tipo = self.__attribute_types[attr_name]
            stream_def_parts.append(f"{attr_name} {tipo}")
        atributos_str = ", ".join(stream_def_parts)
        return f"define stream {self.stream_name}({atributos_str});"

    def get_attributes(self):
        return self.__attribute_types

    def get_attribute_names(self):
        return list(self.__attribute_types.keys())

    def get_attribute_type(self, attr_name: str):
        return self.__attribute_types.get(attr_name, "string")

    def has_attribute(self, name: str) -> bool:
        return name in self.__attribute_types