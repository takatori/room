#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import zmq
from zmq.eventloop.ioloop import PeriodicCallback
from abc import ABCMeta
from abc import abstractmethod
from tornado.options import define, options

from room.utils import zmq_base as base
from room.utils.publisher import Publisher

define("out_addr", default="*:5557")

class ParserModule(base.ZmqProcess):

    def __init__(self, bind_addr, parser):
        super().__init__()
        self.bind_addr = bind_addr
        self.sub_stream = None
        self.parser = parser

    def setup(self, keyword):
        super().setup()
        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=keyword.encode('utf-8'))
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.parser))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()

class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, parser):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._parser = parser
        self._publisher = Publisher(options.out_addr)

    def parse(self, *data):
        parsed_data = self._parser.parse(data)
        for category, state in parsed_data:
            self._publisher.send('', category, state)
        
    def stop(self, data):
        self._stop()


class Parser(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, data):
        '''
        @return [tuple(category, state)]
        category in {'sensor', 'appliance'}
        state must {"key": "value"}
        '''
        raise NotImplementedError()

