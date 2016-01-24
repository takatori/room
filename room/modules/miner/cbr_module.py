#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from room.miner import MinerModule, Miner
from room.modules.miner.estimator.case_based_reasoning import CBR as cbr
from room.utils.config import network_config
from room.utils.config import config
from pymongo import MongoClient

class CBRModule(MinerModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder7']['back']),
            send_addr=int(network_config['forwarder5']['front']),                        
            recv_title='cbr',
            send_title='cbr',
            miner=CBR(),
        )

class CBR(Miner):

    def __init__(self):
        self.cbr = cbr()
        self.records = []
        self.db = MongoDB()
        self.load()

    def mining(self, data):
        result = self.cbr.recommend(data, self.records)
        self.add(data) # キューに保存
        self.pop() # 先頭削除
        return result

    def add(self, data):
        self.records.append(data)

    def pop(self):
        self.records.pop(0)
        
    def load(self):
        records = self.db.all()
        print(len(records), records[0])
        for record in records:
            self.add(record)
            
class MongoDB(object):

    def __init__(self):
        self._client     = MongoClient(config['mongo']['host'], int(config['mongo']['port']))
        self._db         = self._client[config['mongo']['db']]
        self._collection = self._db[config['mongo']['collection']]

    def all(self):
        return [record for record in self._collection.find()]

    def restrict(self, start_index=500000): # start_indexより後のレコードを取得する
        return [record for record in self._collection.find()[start_index:]]

    
    
if __name__ == "__main__":
    #process = CBRModule()
    #process.run()
    
    cbr = CBR()
    data = {'timestamp': '2015-12-31 11:06:47.384507+09:00', 'appliances': {'fan': 0.0, 'ceilinglight': 0.0, 'floorlight': 0.0, 'viera': 0.0, 'curtain': 0.0, 'aircon': 0.0}, 'inout': {'arisa': 0.0, 'sakaki': 0.0, 'horihori': 0.0, 'shinsuke': 0.0, 'otokunaga': 0.0, 'tamamizu': 0.0, 'sachio': 0.0, 'masa-n': 0.0, 'takatori': 0.0, 'tabata': 0.0, 'inomoto': 0.0, 'tktk': 0.0, 'usk108': 1.0, 'junho': 0.0, 'masuda': 0.0, 'longniu': 0.0}, 'sensors': {'core02_brightness': 30.30303, 'core02_pressure': 1004.036011, 'core04_brightness': 10.606061, 'core04_temperature': 24.5, 'core01_pir count': 0.0, 'core01_temperature': 21.5, 'core02_humidity': 25.5, 'core01_pressure': 1009.623474, 'core04_pir count': 4.0, 'core04_pressure': 1005.958374, 'core02_pir count': 26.0, 'core01_brightness': 6.060606, 'core02_temperature': 24.0, 'core01_humidity': 20.0, 'core04_humidity': 45.0}}
    start = time.time()
    print(cbr.mining(data))
    elapsed_time = time.time() - start
    print("elapsed_time:{0}[sec]".format(elapsed_time))
    
