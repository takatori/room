#!/ur/bin/env python3
# -*- coding: utf-8 -*-

import time
import zmq
from abc import ABCMeta
from abc import abstractmethod

from room.utils import zmq_base as base

class DatabaseModule(base.ZmqProcess):
    
    def __init__(self, bind_addr, database):
        super().__init__()
        self.bind_addr = bind_addr
        self.sub_stream = None
        self.db = database
    
    def setup(self, keyword):
        super().setup()
        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=keyword.encode('utf-8'))
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.db))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()
        
class SubStreamHandler(base.MessageHandler):

    def __init__(self, sub_stream, stop, db):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._db = db
        
    def mining(self, *data):
        data = data[1]
        db.save(data)
        
    def stop(self, data):
        self._stop()

        
class Database(metaclass=ABCMeta):

    @abstractmethod
    def save(self, data):
        raise NotImplementedError()
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()        
    
