#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
from zmq.eventloop.ioloop import PeriodicCallback
import time

import zmq_base as base
import state


class ParseProc(base.ZmqProcess):

    def __init__(self, bind_addr):
        super().__init__()

        self.bind_addr = bind_addr
        self.sub_stream = None
        self.publisher = Publisher()
        self.parse_handler = ParseHandler(self.publisher)

    def setup(self):
        super().setup()

        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=b'sparkcore')
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.parse_handler))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()

class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, parse_handler):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._parse_handler = parse_handler

    def parse(self, *data):
        self._parse_handler.parse(data)

    def stop(self, data):
        self._stop()


class ParseHandler(object):

    def __init__(self, publisher):
        self._publisher = publisher
    
    def parse(self, data):
        data = data[1]
        coreId = data['sensorId']
        data.pop('sensorId')
        for key in data.keys():
            self._publisher.send(coreId + "_" + key, data[key])

        
class Publisher(object):

    def __init__(self):
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        self._sock.bind("tcp://*:5557")

        print("Starting broadcast")
        print("Hit Ctrl-C to stop broadcasting.")
        print("Waiting so subscriber sockets can connect...")
        time.sleep(1.0) # SUB は定期的に PUB に接続を見に行くので、少し待つ必要が有る

    def send(self, category, data):
        msg = [category, data]
        self._sock.send_json(data)


if __name__ == "__main__":
    proc = ParseProc('127.0.0.1:5558')
    proc.run()
    
