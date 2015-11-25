#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer.buffer import BufferModule, StateHandler
from room.utils.config import config
from room.utils.log import logging

class TemplateBufferModule(BufferModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), TemlateStateHandler())

    def setup(self):
        super().setup(keyword=config['template_buffer']['keyword'],
                      period=int(config['template_buffer']['interval']))

class TemlateStateHandler(StateHandler):

    def __init__(self):
        super().__init__()
        sensors=["temperature",
                   "humidity",
                   "brightness",
                   "airflow",
                   "w_humidity",
                   "w_light",
                   "w_sound",
                   "w_temperature_c",
                   "w_temperature_f",
                   "out_temperature",
                   "out_humidity",
                   "out_pressure",
                   "out_brightness",
                   "people"]
        
        appliances=["CeilingLight1",
                         "CeilingLight2",
                         "CeilingLight3",
                         "airCleaner",
                         "airConditioner",
                         "airConditionerFront",
                         "aircleaner001",
                         "aircon001",
                         "allLight",
                         "allLight001",
                         "aroma",
                         "aroma001",
                         "dvd001",
                         "fan",
                         "fan001",
                         "floorLight",
                         "floorLight001",
                         "frontCeilingLight",
                         "hddJukeBox",
                         "hddRecorder",
                         "hotCarpet001",
                         "newAirCleaner",
                         "speaker002",
                         "tableLight",
                         "tableLight001",
                         "tv",
                         "tv001",
                         "viera",
                         "windAirCon001"]
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
    proc = TemplateBufferModule(config['parser_buffer_forwarder']['back_port'])
    proc.run()
