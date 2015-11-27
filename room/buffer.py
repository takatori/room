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

    def __init__(self, recv_addr, send_addr, recv_title, send_title, state_handler, period=1000):
        super().__init__()
        self.sub_stream    = None
        self.timer         = None        
        self.recv_addr     = recv_addr
        self.send_addr     = send_addr
        self.recv_title    = recv_title
        self.send_title    = send_title        
        self.state_handler = state_handler
        self.publisher     = Publisher(self.send_addr)
        
    def setup(self):
        super().setup() 
        self.sub_stream, _ = self.stream(zmq.SUB, self.recv_addr, bind=False, subscribe=recv_title.encode('utf-8'))
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.state_handler))
        self.timer = PeriodicCallback(self.publisher.send(self.state_handler), self.period, self.loop)

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

    def sensor(self, data):
        self._state_handler.update_sensor(data)

    def appliance(self, data):
        self._state_handler.update_appliance(data)

    def stop(self, data):
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

    
