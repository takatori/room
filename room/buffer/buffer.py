#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import time
import json
from zmq.eventloop.ioloop import PeriodicCallback
from abc import ABCMeta,abstractmethod

from room.buffer.state import State
from room.utils import zmq_base as base
from room.utils.publisher import Publisher
from room.utils.config import config
from room.utils.log import logging

class BufferModule(base.ZmqProcess):

    def __init__(self, bind_addr, state_handler):
        super().__init__()
        self.bind_addr = bind_addr
        self.sub_stream = None
        self.timer = None
        self.state_handler = state_handler
        
    def setup(self, keyword, period=1000):
        super().setup() 
        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=keyword.encode('utf-8'))
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.state_handler))
        self.timer = PeriodicCallback(self.state_handler, period, self.loop)

    def run(self):
        self.setup()
        print('Start loop!')
        self.timer.start()        
        self.loop.start()

    def stop(self):
        self.loop.stop()

        
class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, state_handler):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._state_handler = state_handler

    def sensor(self, *data):
        logging.info('sensor {0}'.format(data))
        self._state_handler.update_sensor(json.laods(data[1]))

    def appliance(self, *data):
        logging.info('appliance {0}'.format(data))        
        self._state_handler.update_appliance(json.loads(data[1]))

    def stop(self, *data):
        self._stop()


        
class StateHandler(metaclass=ABCMeta):

    def __init__(self):
        self._state = State()
        self._publisher = Publisher(config['buffer_core_forwarder']['front_port'])

    @abstractmethod
    def __call__(self):
        raise NotImplementedError()
    
    @abstractmethod
    def update_sensor(self, data):
        raise NotImplementedError()

    @abstractmethod    
    def update_appliance(self, data):
        raise NotImplementedError()

    
