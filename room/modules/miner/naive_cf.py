#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.miner import MinerModule, Miner
from room.modules.miner.naive_cf_data import NaiveCFData
from room.modules.miner.estimator import collaborative_filtering as cf
from room.utils.config import network_config

class NaiveCollaborativeFilteringModule(MinerModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder4']['back']),
            send_addr=int(network_config['forwarder5']['front']),                        
            recv_title='',
            send_title='',
            miner=NaiveCollaborativeFiltering(),
        )

class NaiveCollaborativeFiltering(Miner):

    def __init__(self):
        self._data = NaiveCFData()
        self.load()

    def mining(self, data):
        df = self._data.add(data) # dataに追加
        index = len(data['sensors'].keys())
        sensor_df, appliance_df = self._data.split(df) # dataframeを分割
        return self.recommend(sensor_df.values[0], appliance_df.values[0])
        
    def load(self):
        '''
        DBからログデータを取得し、self._dataにセットする

        '''
        print('Loading log data...')
        print('Complete loading !')
        
    def predict(self, current_sensor):
        '''
        協調フィルタリングによる家電状態の予測をおこなう

        @return 
        '''
        return cf.predict_appliance_status(
            self._data.sensors(),
            self._data.appliances(),
            current_sensor)

    def recommend(self, current_sensor, appliance_status):
        '''
        協調フィルタリングによる家電状態の推薦をおこなう

        @return 
        '''
        return cf.recommend(
            self._data.sensors(),
            self._data.appliances(),
            current_sensor,
            appliance_status
        )
    
if __name__ == "__main__":
    process = NaiveCollaborativeFilteringModule()
    process.run()
    
    
