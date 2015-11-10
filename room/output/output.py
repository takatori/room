#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from room.utils import zmq_base as base

class OutputModule(base.ZmqProcess):

    def __init__(self, bind_addr, action):
        super().__init__()
        self.bind_addr = bind_addr
        self.sub_stream = None
        self.action = action

    def setup(self, keyword):
        super().setup()
        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=keyword.encode('utf-8'))
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.action))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()
    
class SubStreamHandler(base.MessageHandler):

    def __init__(self, sub_stream, stop, action):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._action = action

    def action(self, *data):
        self._action.action(data)

    def stop(self, data):
        self._stop()


class Action(metaclass=ABCMeta):

    @abstractmethod
    def action(self, data):
        raise NotImplementedError()    
    
