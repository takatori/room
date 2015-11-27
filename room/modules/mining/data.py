#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from room.utils import converter

class Data:
    '''
    過去のログデータをメモリ上に格納するクラス

    '''

    # コンストラクタ
    def __init__(self, data=pd.DataFrame(), sensor_list=[], appliance_list=[]):

        assert isinstance(data, pd.core.frame.DataFrame), 'type error: ' + str(type(data)) + ' != pandas.core.frame.DataFrame'
        
        self.__data = data # DataFrame
        self.__sensor_list = sensor_list # センサデータの種類(説明変数)
        self.__appliance_list = appliance_list # 家電データの種類(目的変数)

    def __str__(self):
        '''
        DataFrameを文字列化する

        '''
        return str(self.__data)

        
    def sensors(self):
        '''
        DataFrameの中からsensorデータの列のみを返す

        @return pd.core.frame.DataFrame
        '''
        return self.__data.ix[:, :len(self.__sensor_list)]


    def appliances(self):
        '''
        DataFrameの中からapplianceデータの列のみを返す

        @return pd.core.frame.DataFrame
        '''        
        return self.__data.ix[:, len(self.__sensor_list):]


    def set(self):
        '''
        DataFrameの全てのデータを返すがsensorデータとapplianceデータを分割して返す

        @return tuple
        '''
        return (self.sensors(), self.appliances())


    def all(self):
        '''
        DataFrameの全てのデータを返す

        @return pd.core.frame.DataFrame
        '''
        return self.__data

    
    def add(self, new):
        '''
        DataFrameに新しいデータを追加する

        '''
        assert isinstance(new, pd.core.frame.DataFrame), 'type error: ' + str(type(new)) + ' != pandas.core.frame.DataFrame'        
        self.__data.append(new)

        
