#!/usr/bin/env python3
# -*- coding: utf-8- 

import unittest
import zmq
import time
from room.utils.publisher import Publisher
from zmq.utils import jsonapi as json

class Subscriber():

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://127.0.0.1:5556')
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        time.sleep(1.0)
        
    def recv(self):
        return self.socket.recv_multipart()
     
        

class PublisherTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.publisher = Publisher('127.0.0.1:5556')
        cls.subscriber = Subscriber()
        
    def test_send(self):
        self.publisher.send('test', 'method', '{"temp": 20, "humid": 30}')
        result = self.subscriber.recv()
        self.assertEqual(result[0], b'test') # data_type
        
        msg = json.loads(result[1])
        self.assertEqual(msg[0], 'method')
        
        data = json.loads(msg[1])
        self.assertEqual(data['temp'], 20)
        self.assertEqual(data['humid'], 30)        

        
if __name__ == '__main__':
    unittest.main()        
        
