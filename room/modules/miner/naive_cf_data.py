#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import json

pd.set_option('max_columns', 500) 
pd.set_option('line_width', 500)    

class NaiveCFData:

    def __init__(self):
        sensor_list = [
            "core01_pressure",
            "core01_pir count",
            "core01_brightness",
            "core01_humidity",
            "core01_temperature",
            "core02_pressure",
            "core02_pir count",
            "core02_brightness",
            "core02_humidity",
            "core02_temperature",
            "core04_pressure",
            "core04_pir count",
            "core04_brightness",
            "core04_humidity",
            "core04_temperature",
            "takatori",
            "tamamizu",
            "tktk",
            "usk108",
            "masuda",
            "otokunaga",
            "sachio",
            "sakaki",
            "shinsuke",
            "tabata",
            "masa-n",
            "longniu",
            "junho",
            "inomoto",
            "horihori",
            "arisa"
        ]

        appliance_list = ["aircon", "viera", "fan", "floorlight", "curtain"]

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

        
    
