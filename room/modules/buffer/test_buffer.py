#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer.buffer import BufferModule, StateHandler
from room.utils.config import config
from room.utils.log import logging

class TestBufferModule(BufferModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), TestStateHandler())

    def setup(self):
        super().setup(keyword=config['template_buffer']['keyword'],
                      period=int(config['template_buffer']['interval']))

class TestStateHandler(StateHandler):

    def __init__(self):
        super().__init__()
        sensors=[
            "core01_pressure",
            "core01_pir count",
            "core01_brightness",
            "core01_humidity",
            "core01_temperature",
            "core02_pressure",
            "core02_pir count",
            "core02_brightness",
            "core02_humidity",
            "core02_temperature",
            "core04_pressure",
            "core04_pir count",
            "core04_brightness",
            "core04_humidity",
            "core04_temperature",
            "takatori",
            "tamamizu",
            "tktk",
            "usk108",
            "masuda",
            "otokunaga",
            "sachio",
            "sakaki",
            "shinsuke",
            "tabata",
            "masa-n",
            "longniu",
            "junho",
            "inomoto",
            "horihori",
            "arisa"
        ]
        
        appliances=["aircon", "viera", "fan", "floorlight", "curtain"]
        self._state.format_sensors(sensors, 0.0)
        self._state.format_appliances(appliances, 0)

    def __call__(self):
        self._publisher.send('', 'mining', self._state.to_json_at_now())        
    
    def update_sensor(self, data):
        key,value = list(data.items())[0]
        self._state.update_sensor(key, value)

    def update_appliance(self, data):
        key,value = list(data.items())[0]        
        self._state.update_appliance(key, value)

    def get_sensor(self):
        return self._state._sensor_state

    def get_appliance(self):
        return self._state._applianece_state
        
if __name__ == "__main__":
    proc = TestBufferModule(config['parser_buffer_forwarder']['back_port'])
    proc.run()
