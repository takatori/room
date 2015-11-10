#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.options import define, options
from room.buffer.buffer import BufferModule, StateHandler

define('buffer_in_addr', default="127.0.0.1:5557")

class DefaultBufferModule(BufferModule):

    def __init__(self, bind_addr):
        super().__init__(bind_addr, DefaultStateHandler())
    
    def setup(self):
        super().setup(keyword='', period=1000)
        
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
    proc = DefaultBufferModule(options.buffer_in_addr)
    proc.run()
