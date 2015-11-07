#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import pytz

class State:
    '''
    センサや家電の状態を保持するクラス

    '''
    def __init__(self):
        self._sensor_state = {} # sensorの状態を保持する辞書
        self._applianece_state = {} # applianceの状態を保持する辞書
        
    def __str__(self):
        return str(self.to_json_at_now())
        
    def update_sensor(self, key, value):
        '''
        sensorの状態を更新する

        '''
        self._sensor_state[key] = value

    def update_appliance(self, key, value):
        '''
        applianceの状態を更新する

        '''        
        self._applianece_state[key] = value

    def get_sensor_keys(self):
        '''
        sensorの種類を取得する

        @return dict_keys
        '''
        return self._sensor_state.keys()

    def get_appliance_keys(self):
        '''
        applianceの種類を取得する

        @return dict_keys
        '''        
        return self._applianece_state.keys()

    def get_sensor_value(self, key):
        return self._sensor_state[key]

    def get_appliance_value(self, key):
        return self._applianece_state[key]
    
    def to_json(self):
        '''
        sensor, applianceの状態をjsonにして返す

        @return str
        '''                
        return json.dumps(
            {
                "sensors": self._sensor_state,
                "appliances": self._applianece_state
            }, sort_keys=True)

    def to_json_with_timestamp(self, time):
        '''
        timestampを付与してjsonで返す

        @return str
        '''
        return json.dumps(
            {
                "timestamp": str(time),
                "sensors": self._sensor_state,
                "appliances": self._applianece_state
            }, sort_keys=True)


    def to_json_at_now(self):
        '''
        現在の時刻をタイムスタンプとしてjsonを返す

        @return str
        '''
        tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz)
        return self.to_json_with_timestamp(now)
    
