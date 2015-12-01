#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import filter
from room.utils.config import network_config

class NaiveCFFilterModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder3']['back']),
            send_addr=int(network_config['forwarder4']['front']),            
            recv_title='',
            send_title='',
            filter=NaiveCFFilter()
        )


class NaiveCFFilter(filter.Filter):

    def __init__(self):

        self.sensors = [
            "core01_pressure",
            "core01_pir count",
            "core01_brightness",
            "core01_humidity",
            "core01_temperature",
            "core02_pressure",
            "core02_pir count",
            "core02_brightness",
            "core02_humidity",
            "core02_temperature",
            "core04_pressure",
            "core04_pir count",
            "core04_brightness",
            "core04_humidity",
            "core04_temperature",
            "takatori",
            "tamamizu",
            "tktk",
            "usk108",
            "masuda",
            "otokunaga",
            "sachio",
            "sakaki",
            "shinsuke",
            "tabata",
            "masa-n",
            "longniu",
            "junho",
            "inomoto",
            "horihori",
            "arisa"
        ]

        self.appliances = [
            "aircon", "viera", "fan", "floorlight", "curtain", "ceilingLight"
        ]
        

    def filtrate(self, data):

        filtered_sensors = {}
        filtered_appliances = {}
        
        for sensor in self.sensors:
            filtered_sensors[sensor] = data['sensors'][sensor] if sensor in data['sensors'] else 0

        for appliance in self.appliances:
            filtered_appliances[appliance] = data['appliances'][appliance] if appliance in data['appliances'] else 0

        return {"timestamp": data['timestamp'], "sensors": filtered_sensors, "appliances": filtered_appliances}


if __name__ == "__main__":
    process =  NaiveCFFilterModule()
    process.run()
