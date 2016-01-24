#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from room.buffer import BufferModule, StateHandler
from room.state import State
from room.utils.config import config
from room.utils.config import network_config

class CBRBufferModule(BufferModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder3']['back']),
            send_addr=int(network_config['forwarder7']['front']),
            recv_title='buffer',
            send_title='cbr',
            state_handler=CBRStateHandler(),
            period=int(config['cbr_buffer']['interval_ms'])
        )
        
class DataStateHandler(StateHandler):

    def __init__(self):
        self._records = []
    
        
    def dump(self):

        sum = {}
        sum['appliances'] = {}
        sum['sensors'] = {}
        sum['inout'] = {}
        
        result = {}
        result['appliances'] = {}
        result['sensors'] = {}
        result['inout'] = {}
        
        num = len(self._records)
        mid = num // 2
        
        for record in self._records:
            for key, value in record['appliances'].items():
                if key not in sum['appliances']: sum['appliances'][key] = value
                else: sum['appliances'][key] += value
            for key, value in record['sensors'].items():
                if key not in sum['sensors']: sum['sensors'][key] = value                
                else: sum['sensors'][key] += value            
            for key, value in record['inout'].items():
                if key not in sum['inout']: sum['inout'][key] = value                                
                else: sum['inout'][key] += value            
            
        for key in sum['appliances'].keys():
            result['appliances'][key] = sum['appliances'][key] / num
        for key in sum['sensors'].keys():
            result['sensors'][key] = sum['sensors'][key] / num
        for key in sum['inout'].keys():
            result['inout'][key] = sum['inout'][key] / num            

        print(str(sum))
        result['timestamp'] = self._records[mid]['timestamp']
                
        self._records.clear()
        
        return result

    def buffering(self, data):
        self._records.append(data)

if __name__ == "__main__":
    #process = DataBufferModule()
    #process.run()

    ds = DataStateHandler()
    data1 = {'timestamp': '2015-12-31 11:06:47.384507+09:00', 'appliances': {'fan': 0.0, 'ceilinglight': 0.0, 'floorlight': 0.0, 'viera': 0.0, 'curtain': 0.0, 'aircon': 0.0}, 'inout': {'arisa': 0.0, 'sakaki': 0.0, 'horihori': 0.0, 'shinsuke': 0.0, 'otokunaga': 0.0, 'tamamizu': 0.0, 'sachio': 0.0, 'masa-n': 0.0, 'takatori': 0.0, 'tabata': 0.0, 'inomoto': 0.0, 'tktk': 0.0, 'usk108': 1.0, 'junho': 0.0, 'masuda': 0.0, 'longniu': 0.0}, 'sensors': {'core02_brightness': 30.30303, 'core02_pressure': 1004.036011, 'core04_brightness': 10.606061, 'core04_temperature': 24.5, 'core01_pir count': 0.0, 'core01_temperature': 21.5, 'core02_humidity': 25.5, 'core01_pressure': 1009.623474, 'core04_pir count': 4.0, 'core04_pressure': 1005.958374, 'core02_pir count': 26.0, 'core01_brightness': 6.060606, 'core02_temperature': 24.0, 'core01_humidity': 20.0, 'core04_humidity': 45.0}}
    data2 = {'timestamp': '2015-12-31 11:06:47.384507+09:00', 'appliances': {'fan': 0.0, 'ceilinglight': 0.0, 'floorlight': 0.0, 'viera': 0.0, 'curtain': 0.0, 'aircon': 0.0}, 'inout': {'arisa': 0.0, 'sakaki': 0.0, 'horihori': 0.0, 'shinsuke': 0.0, 'otokunaga': 0.0, 'tamamizu': 0.0, 'sachio': 0.0, 'masa-n': 0.0, 'takatori': 0.0, 'tabata': 0.0, 'inomoto': 0.0, 'tktk': 0.0, 'usk108': 1.0, 'junho': 0.0, 'masuda': 0.0, 'longniu': 0.0}, 'sensors': {'core02_brightness': 30.30303, 'core02_pressure': 1004.036011, 'core04_brightness': 10.606061, 'core04_temperature': 24.5, 'core01_pir count': 0.0, 'core01_temperature': 21.5, 'core02_humidity': 25.5, 'core01_pressure': 1009.623474, 'core04_pir count': 4.0, 'core04_pressure': 1005.958374, 'core02_pir count': 26.0, 'core01_brightness': 6.060606, 'core02_temperature': 24.0, 'core01_humidity': 20.0, 'core04_humidity': 45.0}}
    data3 = {'timestamp': '2015-12-31 11:06:47.384507+09:00', 'appliances': {'fan': 0.0, 'ceilinglight': 0.0, 'floorlight': 0.0, 'viera': 0.0, 'curtain': 0.0, 'aircon': 0.0}, 'inout': {'arisa': 0.0, 'sakaki': 0.0, 'horihori': 0.0, 'shinsuke': 0.0, 'otokunaga': 0.0, 'tamamizu': 0.0, 'sachio': 0.0, 'masa-n': 0.0, 'takatori': 0.0, 'tabata': 0.0, 'inomoto': 0.0, 'tktk': 0.0, 'usk108': 1.0, 'junho': 0.0, 'masuda': 0.0, 'longniu': 0.0}, 'sensors': {'core02_brightness': 30.30303, 'core02_pressure': 1004.036011, 'core04_brightness': 10.606061, 'core04_temperature': 24.5, 'core01_pir count': 0.0, 'core01_temperature': 21.5, 'core02_humidity': 25.5, 'core01_pressure': 1009.623474, 'core04_pir count': 4.0, 'core04_pressure': 1005.958374, 'core02_pir count': 26.0, 'core01_brightness': 6.060606, 'core02_temperature': 24.0, 'core01_humidity': 20.0, 'core04_humidity': 45.0}}
    data4 = {
        "appliances": {
            "ceilinglight": 0,
            "aircon": 1,
            "curtain": 1,
            "fan": 0,
            "floorlight": 0,
            "viera": 0
        },
        "timestamp": "2016-01-24 14:15:12.598056+09:00",
        "inout": {
            "otokunaga": 0,
            "masa-n": 0,
            "inomoto": 0,
            "junho": 0,
            "tabata": 0,
            "tamamizu": 0,
            "sachio": 0,
            "takatori": 1,
            "horihori": 0,
            "masuda": 0,
            "longniu": 1,
            "shinsuke": 0,
            "usk108": 0,
            "arisa": 1,
            "tktk": 0,
            "time": 0,
            "sakaki": 0
        },
        "sensors": {
            "core01_pressure": 997.896118,
            "core02_pressure": 995.804932,
            "core01_pir count": 0,
            "core04_pressure": 999.506348,
            "core02_humidity": 13.3,
            "core04_brightness": 37.878788,
            "core04_pir count": 0,
            "core01_temperature": 26.200001,
            "core04_temperature": 23.9,
            "core01_brightness": 30.30303,
            "core01_humidity": 10.4,
            "core04_humidity": 13.3,
            "core02_brightness": 36.363636,
            "core02_pir count": 0,
            "core02_temperature": 23.1
        }
    }
    ds.buffering(data1)
    ds.buffering(data2)
    ds.buffering(data3)
    ds.buffering(data4)
    print(ds.dump())
    
