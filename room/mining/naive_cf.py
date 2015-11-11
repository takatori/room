#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.mining.mining import MiningModule, MiningHandler
from room.utils import converter
from room.mining.data import Data
from room.mining.estimator import collaborative_filtering as cf
from room.utils.config import config

class NaiveCollaborativeFilteringModule(MiningModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), NaiveCollaborativeFiltering())

    def setup(self):
        super().setup('')

class NaiveCollaborativeFiltering(MiningHandler):

    def __init__(self):
        self._data = None
        self.load()

    def mining(self, data):
        df = converter.dict_to_df(data)
        self.add(df)
        index = len(data['sensors'].keys())
        sensor_df, appliance_df = converter.partition(df,index) # dataframeを分割
        return self.predict(sensor_df.values[0])
        
    def load(self):
        '''
        DBからログデータを取得し、self._dataにセットする

        '''
        print('Loading log data...')        
        self._data = Data()
        print('Complete loading !')
        
    def add(self, df):
        '''
        self._dataにデータを追加する

        '''
        self._data.add(df)

    def show(self):
        self._data.all()
        
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
        return cf.reccomend(
            self._data.sensors(),
            self._data.appliances(),
            current_sensor,
            appliance_status
        )
    
if __name__ == "__main__":
    proc = NaiveCollaborativeFilteringModule('localhost:{0}'.format(config['buffer_core_forwarder']['back_port']))
    proc.run()
    
    
