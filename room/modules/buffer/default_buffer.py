#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer import BufferModule, StateHandler
from room.state import State
from room.utils.config import config
from room.utils.config import network_config

class DefaultBufferModule(BufferModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder2']['back']),
            send_addr=int(network_config['forwarder3']['front']),
            recv_title='',
            send_title='naive_cf',
            state_handler=DefaultStateHandler(),
            period=int(config['default_buffer']['interval'])
        )
        
class DefaultStateHandler(StateHandler):

    def __init__(self):
        self._state = State()
        
    def dump(self):
        return self._state.dump_at_now()

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
    process = DefaultBufferModule()
    process.run()
