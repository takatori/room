#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import json

from room.utils import zmq_base as base
from room.utils import converter
from room.mining.estimator import collaborative_filtering as cf
from room.mining.data import Data
from room.utils.publisher import Publisher
from room.utils.config import config
from room.utils.log import logging

class MiningModule(base.ZmqProcess):

    def __init__(self, bind_addr):
        super().__init__()

        self.bind_addr = bind_addr
        self.sub_stream = None
        self.mining_handler = MiningHandler()

    def setup(self):
        super().setup()

        self.sub_stream, _ = self.stream(zmq.SUB, self.bind_addr, bind=False, subscribe=b'')
        self.sub_stream.on_recv(SubStreamHandler(self.sub_stream, self.stop, self.mining_handler))

    def run(self):
        self.setup()
        print('Start loop!')
        self.loop.start()

    def stop(self):
        self.loop.stop()


class SubStreamHandler(base.MessageHandler):
    
    def __init__(self, sub_stream, stop, mining_handler):
        super().__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._mining_handler = mining_handler
        self._publisher = Publisher(config['core_output_forwarder']['front_port'])

    def mining(self, *data):
        logging.info(data)
        data = json.loads(data[1])
        df = converter.dict_to_df(data)
        self._mining_handler.add(df)
        index = len(data['sensors'].keys())
        sensor_df, appliance_df = converter.partition(df,index) # dataframeを分割
        result = self._mining_handler.predict(sensor_df.values[0])
        self._publisher.send('', 'output', str(result))

        
    def stop(self, data):
        self._stop()

class MiningHandler(object):

    def __init__(self):
        self._data = None
        self.load()

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
    proc = MiningModule('localhost:{0}'.format(config['buffer_core_forwarder']['back_port']))
    proc.run()
    
