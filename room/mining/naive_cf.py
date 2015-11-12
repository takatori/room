#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.mining.mining import MiningModule, MiningHandler
from room.utils import converter
from room.mining.naive_cf_data import NaiveCFData
from room.mining.estimator import collaborative_filtering as cf
from room.utils.config import config

class NaiveCollaborativeFilteringModule(MiningModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), NaiveCollaborativeFiltering())

    def setup(self):
        super().setup()

class NaiveCollaborativeFiltering(MiningHandler):

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
    proc = NaiveCollaborativeFilteringModule(config['buffer_core_forwarder']['back_port'])
    proc.run()
    
    
