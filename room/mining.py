#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import json
from abc import ABCMeta, abstractmethod

from room.utils import zmq_base as base
from room.utils.publisher import Publisher
from room.utils.config import config
from room.utils.log import logging

class MiningModule(base.ZmqProcess):

    def __init__(self, bind_addr, mining_handler):
        super().__init__()

        self.bind_addr = bind_addr
        self.sub_stream = None
        self.mining_handler = mining_handler

    def setup(self):
        super().setup()

        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=b'')
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.mining_handler))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()


class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, mining_handler):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._mining_handler = mining_handler
        self._publisher = Publisher(config['core_output_forwarder']['front_port'])

    def mining(self, *data):
        logging.info(data)
        data = json.loads(data[1])
        result = self._mining_handler.mining(data)
        self._publisher.send('', 'output', str(result))
        
    def stop(self, data):
        self._stop()

class MiningHandler(metaclass=ABCMeta):

    @abstractmethod
    def mining(self, data):
        raise NotImplementedError()            
    
