#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer.buffer import BufferModule, StateHandler
from room.utils.config import config

class DefaultBufferModule(BufferModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), DefaultStateHandler())
    
    def setup(self):
        super().setup(keyword=config['default_buffer']['keyword'],
                      period=int(config['default_buffer']['interval']))
        
class DefaultStateHandler(StateHandler):
        
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
    proc = DefaultBufferModule(config['parser_buffer_forwarder']['back_port'])
    proc.run()
