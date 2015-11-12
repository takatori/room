#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from room.utils import converter
import json

pd.set_option('max_columns', 500) 
pd.set_option('line_width', 500)    

class NaiveCFData:

    def __init__(self):
        sensor_list = ["temperature",
                       "humidity",
                       "brightness",
                       "airflow",
                       "w_humidity",
                       "w_light",
                       "w_sound",
                       "w_temperature_c",
                       "w_temperature_f",
                       "out_temperature",
                       "out_humidity",
                       "out_pressure",
                       "out_brightness",
                       "people"]

        appliance_list = ["CeilingLight1",
                          "CeilingLight2",
                          "CeilingLight3",
                          "airCleaner",
                          "airConditioner",
                          "airConditionerFront",
                          "aircleaner001",
                          "aircon001",
                          "allLight",
                          "allLight001",
                          "aroma",
                          "aroma001",
                          "dvd001",
                          "fan",
                          "fan001",
                          "floorLight",
                          "floorLight001",
                          "frontCeilingLight",
                          "hddJukeBox",
                          "hddRecorder",
                          "hotCarpet001",
                          "newAirCleaner",
                          "speaker002",
                          "tableLight",
                          "tableLight001",
                          "tv",
                          "tv001",
                          "viera",
                          "windAirCon001"]

        self.sensor_list = sensor_list
        self.appliance_list = appliance_list
        self.columns = self.sensor_list + self.appliance_list
        self.__data = pd.DataFrame(columns=self.columns)

    def __str__(self):
        return str(self.__data)
    
    def add(self, data):
        sensors = [data['sensors'][key] for key in self.sensor_list] # python配列は順序が保証されないのでセンサリストの順に並べ替え
        appliances = [data['appliances'][key] for key in self.appliance_list]
        new = np.array(sensors + appliances).astype(float)
        assert len(new) == len(self.columns), 'lack data'
        df = pd.DataFrame([new], columns=self.columns) # 1行のデータフレーム作成
        df.index = pd.to_datetime([data['timestamp']]) # タイムスタンプ付与        
        self.__data = self.__data.append(df) 
        return df

    def split(self, df):
        return (df.ix[:, :len(self.sensor_list)], df.ix[:, len(self.sensor_list):])
    
    def all(self):
        return self.__data

    def sensors(self):
        return self.__data.ix[:, :len(self.sensor_list)]
        
    def appliances(self):
        return self.__data.ix[:, len(self.sensor_list):]        
        
    def set(self):
        return (self.sensors(), self.appliances())


    def drop(self):
        self.__data = self.__data.drop(self.__data.index)

        
    
