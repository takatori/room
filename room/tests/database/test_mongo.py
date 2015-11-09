#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import datetime
from room.database.mongo import MongoDB

class MongoDBTest(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.mongo = MongoDB()

    def test_save(self):
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}
        self.mongo.save(post)
        
    def test_load(self):
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}
        self.mongo.save(post)
        result = self.mongo.load()
        self.assertEqual(result[0]['author'], "Mike")
        self.assertEqual(result[0]['text'], "My first blog post!")
        
    @classmethod
    def tearDownClass(cls):
        cls.mongo.drop()

    
if __name__ == '__main__':
    unittest.main()
