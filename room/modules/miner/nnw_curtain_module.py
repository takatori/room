#!/usr/bin/env python
# -*- coding: utf-8 -*-

from room.miner import MinerModule, Miner
from room.modules.miner.estimator.nnw import NeuralNetWork as NNW
from room.utils.config import network_config

class NNWModule(MinerModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder3']['back']),
            send_addr=int(network_config['forwarder4']['front']),
            recv_title='nnw',
            send_title='nnw',
            miner=NeuralNetWork(),
        )


class NeuralNetWork(Miner):

    def __init__(self):
        self.appliance = 'curtain'        
        self.nnw = NNW(self.appliance)

    def mining(self, data):
        result = self.nnw.predict(data['data'])
        
        if result:
            return {self._appliance:result} # tuple to dict
        else:
            return []

    

if __name__ == "__main__":
    process = NNWModule()
    process.run()
    
    

