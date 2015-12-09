#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import filter
from room.utils.config import network_config

class RecommendAggregatorModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder5']['back']),
            send_addr=int(network_config['forwarder6']['front']),            
            recv_title='',
            send_title='',
            filter=RecommendAggregator()
        )


class RecommendAggregator(filter.Filter):

    def __init__(self):
        # 一つ前のレコメンドのリスト
        # ex: set([(viera, on), (fan, off)])
        self.previous_recommends = set()

        
    def filtrate(self, data):
        dataset = set(data) # list to set
        result = dataset.difference(self.previous_recommends) # 差集合
        self.previous_recommends = dataset 
        return list(result)
        
        
if __name__ == "__main__":
    process =  RecommendAggregatorModule()
    process.run()
