#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

from room import database
from room.utils.config import config

class MongoModule(database.DatabaseModule):

    def __init__(self, port):
        super().__init__(
            recv_addr='localhost:{0}'.format(config['buffer_core_forwarder']['back_port']),
            recv_title=config['mongo']['keyword'],
            db=MongoDB()
        )

class MongoDB(database.Database):

    def __init__(self):
        self._client     = MongoClient(config['mongo']['host'], int(config['mongo']['port']))
        self._db         = self._client[config['mongo']['db']]
        self._collection = self._db[config['mongo']['collection']]
        
    def save(self, data):
        self._collection.insert_one(data)

    def load(self):
        return [record for record in self._collection.find()]

    def drop(self):
        self._collection.delete_many({})

if __name__ == "__main__":
    process = MongoModule()
    process.run()
            
