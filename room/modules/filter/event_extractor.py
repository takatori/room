#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import filter
from room.utils.config import network_config

class EventExtractorModule(filter.FilterModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder2']['back']),
            send_addr=int(network_config['forwarder4']['front']),            
            recv_title='appliance',
            send_title='speed',
            filter=EventExtractor()
        )


class EventExtractor(filter.Filter):
    '''
    状態ログからイベントを抽出するクラス
    状態が変化していたらイベントがあったとみなす
    '''

    def __init__(self):
        self.previous_status = {} # イベントごとに一つ前の状態を記憶する ex: {'viera': 1}


    def filtrate(self, data):
        '''
        イベントを抽出する
        @override
        @param data: ex: {'viera', 0}
        '''
        if self.previous_status[data[0]] == data[1]:　# 状態が変化していなければNoneを返す
            return {}
        else:
            self.previous_status[data[0]] = data[1] # 保持している状態を変更する
            return data



        
