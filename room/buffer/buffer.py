#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
from zmq.eventloop.ioloop import PeriodicCallback
import time
from tornado.options import define, options

from room.utils import zmq_base as base
from room.buffer.state import State

class BufferModule(base.ZmqProcess):

    def __init__(self, bind_addr):
        super().__init__()

        self.bind_addr = bind_addr
        self.sub_stream = None
        self.timer = None
        self.state = State()
        self.buffer_handler = BufferHandler(self.state)
        self.publisher = Publisher(self.state)
        
    def setup(self):
        super().setup()

        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=b'')
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.buffer_handler))

        self.timer = PeriodicCallback(self.publisher, 1000, self.loop)

    def run(self):
        self.setup()
        print('Start loop!')
        self.timer.start()        
        self.loop.start()

    def stop(self):
        self.loop.stop()

class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, buffer_handler):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._buffer_handler = buffer_handler

    def sensor(self, data):
        self._buffer_handler.update_sensor(data)

    def appliance(self, data):
        self._buffer_handler.update_appliance(data)        

    def stop(self, data):
        self._stop()

class BufferHandler(object):

    def __init__(self, state):
        self._state = state

    def sensor(self, data):
        self._state.update_sensor()

    def appliance(self, data):
        self._state.update_appliance()

        
class Publisher(object):

    def __init__(self, state):
        self._state = state
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        self._sock.bind("tcp://*:5556")

        print("Starting broadcast")
        print("Hit Ctrl-C to stop broadcasting.")
        print("Waiting so subscriber sockets can connect...")
        time.sleep(1.0) # SUB は定期的に PUB に接続を見に行くので、少し待つ必要が有る

    def __call__(self):
        self.send()
    
        
    def send(self):
        msg = ['mining', self._state.to_json_at_now()]
        self._sock.send_json(msg)

        
if __name__ == "__main__":
    proc = BufferModule('127.0.0.1:5557')
    proc.run()

    
