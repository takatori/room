#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import time
from zmq.utils import jsonapi as json

class Publisher(object):

    def __init__(self, bind_addr):
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        self._sock.bind("tcp://" + bind_addr)

        print("Starting broadcast")
        print("Hit Ctrl-C to stop broadcasting.")
        print("Waiting so subscriber sockets can connect...")
        time.sleep(1.0) # SUB は定期的に PUB に接続を見に行くので、少し待つ必要が有る

    def send(self, data_type, method, data):
        msg = json.dumps([method, data])
        data = [data_type.encode('utf-8'), msg]
        self._sock.send_multipart([data_type.encode('utf-8'), msg])
