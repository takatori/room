#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import filter
from room.utils.config import network_config

class RecommendAggregatorModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder4']['back']),
            send_addr=int(network_config['forwarder5']['front']),            
            recv_title='cbr',
            send_title='',
            filter=RecommendAggregator()
        )


class RecommendAggregator(filter.Filter):
    '''
    連続したレコメンドを一つに集約するためのフィルタ
    一つ前のレコメンド集合と現在のレコメンド集合の
    差分があればそのレコメンドを含む配列を返す
    差分がなければ空配列を返す

        current                              prev                                     out
    [('viera,'on'), ('fan','on')]             []                        [('viera,'on'), ('fan','on')]
    [('viera,'on')]                [('viera,'on'), ('fan','on')]                       []
    [('viera,'on')]                     [('viera,'on')]                                []
    '''

    def __init__(self):
        # 一つ前のレコメンドのリスト
        # ex: set([(viera, on), (fan, off)])
        self.previous_recommends = set()

        
    def filtrate(self, data):
        dataset = set([(recommend['appliance'], recommend['method']) for recommend in data]) # list[dict] to set
        
        # 差集合
        # (現在のレコメンド群) - (一つ前のレコメンド群) = (新しく追加されたレコメンド)
        result = dataset.difference(self.previous_recommends) 
        self.previous_recommends = dataset
        
        return [{'appliance': recommend[0], 'method': recommend[1]} for recommend in result] # to json format    
        
        
if __name__ == "__main__":
    process =  RecommendAggregatorModule()
    process.run()
