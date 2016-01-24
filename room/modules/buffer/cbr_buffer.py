#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer import BufferModule, StateHandler
from room.state import State
from room.utils.config import config
from room.utils.config import network_config

class CBRBufferModule(BufferModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder2']['back']),
            send_addr=int(network_config['forwarder3']['front']),
            recv_title='',
            send_title='buffer',
            state_handler=CBRStateHandler(),
            period=int(config['cbr_buffer']['interval_ms'])
        )
        
class CBRStateHandler(StateHandler):

    def __init__(self):
        self._state = State()
        
    def dump(self):
        return self._state.dump_at_now()

    def buffering(self, data):
        category = data['category']
        key,value = list(data['msg'].items())[0]

        if category == 'sensor':
            self._state.update_sensor(key, value)
        elif category == 'inout':
            self._state.update_inout(key, value)           
        elif category == 'appliance':
            self._state.update_appliance(key, value)



if __name__ == "__main__":
    process = CBRBufferModule()
    process.run()
