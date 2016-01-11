#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.miner import MinerModule, Miner
from room.modules.miner.estimator.case_based_reasoning import CBR as cbr
from room.utils.config import network_config

class CBRModule(MinerModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder3']['back']),
            send_addr=int(network_config['forwarder4']['front']),                        
            recv_title='',
            send_title='cbr',
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
    process = CBRModule()
    process.run()
