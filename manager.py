from PySiddhi.core.SiddhiManager import SiddhiManager

class SiddhiAppManager:
    def __init__(self, siddhi_app: str):
        self.manager = SiddhiManager()
        self.runtime = self.manager.createSiddhiAppRuntime(siddhi_app)

    def add_callback(self, query_name: str, callback):
        self.runtime.addCallback(query_name, callback)

    def get_input_handler(self, stream_name: str):
        return self.runtime.getInputHandler(stream_name)

    def start(self):
        self.runtime.start()

    def shutdown(self):
        self.manager.shutdown()
