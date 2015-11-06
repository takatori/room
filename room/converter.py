#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import libraries
import pandas as pd
import numpy as np
import csv
import sys
from dateutil.parser import parse
from datetime import timedelta
import pytz
import json

def concat(dataframes):
    '''
    ２つのDataFrameを列方向に結合してNAを含む行を削除

    @ return pandas.DataFrame
    '''
    return pd.concat(dataframes, axis=1).dropna() # NAを含む行を削除する

def attach_timestamp_to_index(df, time_column):
    '''
    DataFrameの指定された列の値をtimestampとしてindexに張り替える
    '''
    assert isinstance(df, pd.core.frame.DataFrame), 'type error: ' + str(type(df)) + ' != pandas.core.frame.DataFrame'    
    df.index = pd.to_datetime(df[time_column])
    df.drop(time_column, axis=1, inplace=True)
    return df


def resample(df, sampling_type="under"):
    '''
    再サンプリング
    一分間ごとに平均をとる
    オーバーサンプリングならNAを含む行を削除
    アンダーサンプリングならNAを0で埋める
    '''
    assert isinstance(df, pd.core.frame.DataFrame), 'type error: ' + str(type(df)) + ' != pandas.core.frame.DataFrame'

    if type == "over":
        return df.resample('1min', how="mean").fillpna(0)
    
    return df.resample('1min', how="mean").dropna() 

def oversample(df):
    '''
    オーバーサンプリング
    一分間ごとに平均をとる
    '''
    assert isinstance(df, pd.core.frame.DataFrame), 'type error: ' + str(type(df)) + ' != pandas.core.frame.DataFrame'
    return df.resample('1min', how="mean").fillpna() 


def cast_sensorlog(record):
    '''
    センサログの型変換を行う
    
    '''
    return [record[0] + " " + record[1]] + [float(x) for x in record[2:]]

def sensorlog_to_df(sensorlog):
    '''
    sensorlogを読み込んでpandas.DataFrameに変換する

    @return　pandas.DataFrame
    '''
    assert isinstance(sensorlog, list), 'type error: ' + str(type(sensorlog)) + ' != list'

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

    result = [cast_sensorlog(line) for line in sensorlog]
    return pd.DataFrame(result, columns=['timestamp'] + sensor_list)
    
def sensorlog_to_resampled_df(sensorlog):
    df = sensorlog_to_df(sensorlog)
    indexed_df = attach_timestamp_to_index(df, 'timestamp')
    return resample(indexed_df)


def cast_sparkcorelog(record):
    '''
    transform sparkcore sensorlog data
                            from 
    --------------------------------------------------------------------
    id,temperature,humidity,pressure,brightness,pircount,timestamp
    core01,29.6,34.700001,988.934937,42.424244,4,2015-09-25T04:51:23.000Z
    --------------------------------------------------------------------
                             to
    --------------------------------------------------------------------
    ['2015-10-07 16:51:49+09:00', 31.0, 20.4, 996.541809, 43.939392, 19.0]
    --------------------------------------------------------------------

    '''
    # 文字列タイムスタンプをtimedateオブジェクトに変換しtimezoneを付与、最後にもう一度文字列に変換
    # センサの値を文字列からfloat値に変換    
    return [str(parse(record[-1]).astimezone(pytz.timezone('Asia/Tokyo')))] + [float(x) for x in record[1:-1]]

def sparkcorelog_to_df(sparkcorelog):

    sensor_id = sparkcorelog[0][0]
    sensor_list = ['temp','hum','pres','bright','pir']
    result = [cast_sparkcorelog(line) for line in sparkcorelog]
    return pd.DataFrame(result, columns=['timestamp'] + [ sensor_id + '_' + x for x in sensor_list])


def sparkcorelogs_to_resampled_df(sparkcorelogs):
    return concat([
        resample(
            attach_timestamp_to_index(
                sparkcorelog_to_df(log), 'timestamp'))
        for log in sparkcorelogs
    ])
     


def cast_appliancelog(record, method_list):
    '''
    transform appliancelog data　(1 of K)

                from csv
    ----------------------------------
    date, time, appliance, method
    "2015-09-25","09:10:08","Viera","off"
    ----------------------------------
                 to array
    ----------------------------------------------------------------------------------------
    [timestamp, Viera on, Viera off, CeilingLights on, CeilingLights off, Curtain open, Curatain close, ...]
    ["2015-09-25 09:10:08 +09:00", 0, 1, 0, 0, 0, 0, 0, ...]
    ----------------------------------------------------------------------------------------
    '''
    timestamp = [str(parse(record[0] + " " + record[1] + "+09:00"))]
    method    = record[2] + " " + record[3]
    return timestamp + [1 if method == m else 0 for m in method_list] # 家電と操作名が一致していたら1を返す


def appliancelog_to_df(appliancelog):

    method_list = ["Viera on",
                   "CeilingLights on",
                   "CeilingLights off",                             
                   "Curtain open",
                   "Curatain close",
                   "Fan on",
                   "AirConditionerCeiling on",
                   "AirConditionerCeiling off",
                   "AirConditionerCeiling colding"]
    
    result = [cast_appliancelog(line, method_list) for line in appliancelog]
    return pd.DataFrame(result, columns=['timestamp'] + method_list)

def appliancelog_to_resampled_df(appliancelog):
    cleanlog = cleanse(appliancelog)
    df = appliancelog_to_df(cleanlog)
    indexed_df = attach_timestamp_to_index(df, 'timestamp')
    return resample(indexed_df, 'over')


def cleanse(appliance_list=[]):
    '''
    実験に利用できそうにないデータをフィルタリング
    連続で同じ操作が実行されている場合は最後のログを利用する
    '''
    appliance_list.pop(0)
    # 実験に使わない家電と操作名のリスト
    black_list     = ["Appliance resetStatus",
                      "Viera off",
                      "Viera upVolume",
                      "Viera downVolume",
                      "Viera setChannel",
                      "Viera changeInputScreenSwitching",                       
                      "Fan off",
                      "WeatherGoose <init>"]

    filtered_list = list(filter((lambda x: x[2] + " " + x[3] not in black_list),appliance_list))

    # 連続して同じ家電に同じ操作が行われたログが現れた場合
    # 連続の最後のログ以外は削除する
    for i in range(0, len(filtered_list)-1):
        line = filtered_list[i]
        next_line = filtered_list[i+1]
        if line[2] == next_line[2] and line[3] == next_line[3]:
            filtered_list[i][0] = "delete"

    cleansed_list =  list(filter((lambda x: x[0] != "delete"),filtered_list))

    return cleansed_list


def cast_appliance_statuslog(record, appliance_list):
    timestamp = [record[0] + " " + record[1]]
    appliance = record[2]
    status = record[3]
    return timestamp + [1 if x == appliance and status == "true" else 0 for x in appliance_list]

def appliance_statuslog_to_df(statuslog):
    appliance_list =    ["CeilingLight1",
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
    result = [cast_appliance_statuslog(line, appliance_list) for line in statuslog]
    return pd.DataFrame(result, columns=['timestamp'] + appliance_list)    

def appliance_statuslog_to_resampled_df(statuslog):
    df = appliance_statuslog_to_df(statuslog)
    indexed_df = attach_timestamp_to_index(df, 'timestamp')
    return indexed_df.resample('1min', how='max').dropna()
    

def coordinate(sensorlog, appliance_statuslog):
    return concat([
        sensorlog_to_resampled_df(sensorlog),
        appliance_statuslog_to_resampled_df(appliance_statuslog)])
    
def partition(df, index):
    '''
    データフレームを指定されたサイズで列方向に二つに分割する
    '''
    sensor_df = df.ix[:, :index]
    appliance_df = df.ix[:, index:]
    return (sensor_df, appliance_df)

def convert(sensorlog, appliance_statuslog):
    return partition(coordinate(sensorlog, appliance_statuslog), len(sensorlog[0])-2)


def dict_to_df(data):
    '''
    
    '''
    timestamp = data['time']

    sensor_dict = data['sensors']
    sensor_list = list(sensor_dict.keys())
    sensor_values = list(sensor_dict.values())
    
    appliance_dict = data['appliances']
    appliance_list = list(appliance_dict.keys())
    appliance_values = list(appliance_dict.values())

    return pd.DataFrame(np.array([sensor_values + appliance_values]),
                        index=[timestamp],
                        columns=sensor_list + appliance_list)


    
