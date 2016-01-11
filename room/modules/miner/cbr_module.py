#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.miner import MinerModule, Miner
from room.modules.miner.estimator.case_based_reasoning import CBR as cbr
from room.utils.config import network_config

class CBRModule(MinerModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder4']['back']),
            send_addr=int(network_config['forwarder5']['front']),                        
            recv_title='',
            send_title='',
            miner=CBR(),
        )


class CBR(Miner):

    def __init__(self):
        self.cbr = cbr()
        self.records = []

    def mining(self, data):
        result = self.cbr.recommend(data, self.records)
        self.add(data) # 保存
        return result

    def add(self, data):
        self.records.append(data)

    def load(self):
        pass
    
    
if __name__ == "__main__":
    #process = CBRModule()
    #process.run()

    current = {
        "appliances": {
            "ceilinglight": 0,
            "aircon": 0,
            "fan": 0,
            "curtain": 0,
            "viera": 0,
            "floorlight": 0
        },
        "inout": {
            "sakaki": 0,
            "tamamizu": 0,            
            "inomoto": 0,
            "sachio": 0,
            "junho": 0,
            "tktk": 0,
            "takatori": 1,
            "horihori": 0,
            "otokunaga": 1,
            "tabata": 0,
            "masa-n": 0,
            "usk108": 0,
            "longniu": 0,
            "masuda": 0,
            "shinsuke": 0,
            "arisa": 0            
        },
        "sensors": {
            "core01_brightness": 34.848484,
            "core01_pir count": 0,
            "core04_brightness": 0,
            "core04_pir count": 0,
            "core01_temperature": 26.299999,
            "core04_temperature": 0,
            "core04_humidity": 0,
            "core01_pressure": 1004.775635,
            "core02_pressure": 998.34137,
            "core02_humidity": 23.700001,
            "core01_humidity": 17.4,
            "core02_temperature": 26,
            "core04_pressure": 0,
            "core02_brightness": 28.787878,
            "core02_pir count": 21,
        },
        "timestamp": "2016-01-08 22:08:50.970682+09:00"
    }

    record1 = {
        "appliances": {
            "ceilinglight": 0,
            "aircon": 0,
            "fan": 0,
            "curtain": 1,
            "viera": 0,
            "floorlight": 0
        },
        "inout": {
            "sakaki": 1,
            "tamamizu": 0,            
            "inomoto": 0,
            "sachio": 0,
            "junho": 0,
            "tktk": 0,
            "takatori": 1,
            "horihori": 1,
            "otokunaga": 1,
            "tabata": 0,
            "masa-n": 0,
            "usk108": 1,
            "longniu": 0,
            "masuda": 0,
            "shinsuke": 0,
            "arisa": 0            
        },
        "sensors": {
            "core01_temperature": 27.799999,
            "core01_brightness": 28.787878,
            "core01_pir count": 0,
            "core02_brightness": 12.121212,
            "core01_humidity": 24.6,
            "core04_pressure": 1018.481323,
            "core04_humidity": 31.4,
            "core02_pir count": 1,
            "core04_temperature": 25.1,
            "core02_humidity": 29.799999,
            "core02_temperature": 24.5,
            "core02_pressure": 1014.526245,
            "core04_pir count": 0,
            "core01_pressure": 1016.13501,
            "core04_brightness": 480.30304
        },
        "timestamp": "2016-01-08 20:08:50.970682+09:00"
    }
    
    record2 = {
        "appliances": {
            "ceilinglight": 1,
            "aircon": 0,
            "fan": 0,
            "curtain": 1,
            "viera": 0,
            "floorlight": 0
        },
        "inout": {
            "sakaki": 1,
            "tamamizu": 0,            
            "inomoto": 0,
            "sachio": 0,
            "junho": 0,
            "tktk": 0,
            "takatori": 1,
            "horihori": 1,
            "otokunaga": 1,
            "tabata": 0,
            "masa-n": 0,
            "usk108": 1,
            "longniu": 0,
            "masuda": 0,
            "shinsuke": 0,
            "arisa": 0            
        },
        "sensors": {
            "core01_temperature": 20.799999,
            "core01_brightness": 29.787878,
            "core01_pir count": 0,
            "core02_brightness": 13.121212,
            "core01_humidity": 24.6,
            "core04_pressure": 1018.481323,
            "core04_humidity": 31.4,
            "core02_pir count": 1,
            "core04_temperature": 25.1,
            "core02_humidity": 29.799999,
            "core02_temperature": 24.3,
            "core02_pressure": 1014.526245,
            "core04_pir count": 0,
            "core01_pressure": 1016.13501,
            "core04_brightness": 480.30304
        },
        "timestamp": "2016-01-08 22:08:50.970682+09:00"
    }


    data_list = [current, record1, record2]

    CBR = CBR()
    
    for data in data_list:
        print(CBR.mining(data))
    
        


