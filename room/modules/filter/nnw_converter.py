#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
from dateutil.parser import parse

from room import filter
from room.utils.config import network_config

class NNWConverterModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder3']['back']),
            send_addr=int(network_config['forwarder6']['front']),            
            recv_title='buffer',
            send_title='nnw',
            filter=Converter()
        )


class Converter(filter.Filter):

    def __init__(self):

        self.data_list = [            
            "core01_temperature",
            "core02_temperature",                        
            "core04_temperature",
            "core01_brightness",
            "core02_brightness",
            "core04_brightness",            
            "core01_humidity",
            "core02_humidity",            
            "core04_humidity",
            "core01_pressure",
            "core02_pressure",
            "core04_pressure",            
            "core01_pir count",
            "core02_pir count",
            "core04_pir count",
            "otokunaga",
            "masa-n",
            "inomoto",
            "junho",
            "tabata",
            "tamamizu",
            "sachio",
            "takatori",
            "horihori",
            "masuda",
            "longniu",
            "shinsuke",
            "usk108",
            "arisa",
            "tktk",
            "time",
            "sakaki"            
        ]

        self.target_list = [
            "ceilinglight",
            "aircon",
            "curtain",
            "fan",
            "floorlight",
            "viera"            
        ]

    

    def filtrate(self, data):
        
        sensors = data['sensors'] 
        inout   = data['inout']
        appliances = data['appliances']

        sensors.update(inout) # 2つのdictを結合
        d = [sensors[x] if x in sensors else 0 for x in self.data_list] # data_listの順にvalueを取り出し

        date = parse(record['timestamp']) 
        week = date.weekday() # 日付
        elapsed_minute = date.time().hour * 60 + date.time().minute # 0時0分からの経過分数
        
        d = d + [week, elapsed_minute] # data配列に追加

        d = np.array(d)
        
        return {'data': d, 'target': appliances}
    

    
if __name__ == "__main__":
    process =  NNWConverterModule()
    process.run()

