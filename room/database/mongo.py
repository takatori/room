#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from room.database import database

class MongoModule(database.DatabaseModule):

    def __init__(self, bind_addr):
        super().__init__(bind_addr, MongoDB())

    def setup(self):
        super().setup('mongo')

class MongoDB(database.Database):

    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        self._db = self._client['room']
        self._collection = self._db.test
        
    def save(self, data):
        self._collection.insert_one(data)

    def load(self):
        return [record for record in self._collection.find()]

    def drop(self):
        self._collection.delete_many({})

if __name__ == "__main__":
    proc = MongoModule('127.0.0.1:5556')
    proc.run()
            
