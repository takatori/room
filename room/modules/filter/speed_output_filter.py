#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import filter
from room.utils.config import network_config

class SpeedOutPutFilterModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder4']['back']),
            send_addr=int(network_config['forwarder5']['front']),            
            recv_title='',
            send_title='speed',
            filter=SpeedFilter()
        )


class SpeedFilter(filter.Filter):

    def __init__(self):

        self.inout = [
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

    def filtrate(self, data):

        key = list(data.keys())[0]
        
        if key in self.inout:
            return None
        else:
            return data

if __name__ == "__main__":
    process =  SpeedOutPutFilterModule()
    process.run()
