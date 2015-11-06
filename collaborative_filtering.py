#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
from math import sqrt

def normalize(df):
    '''
    センサデータの正規化
    簡易版

    @ return pandas.DataFrame
    '''
    assert isinstance(df, pd.core.frame.DataFrame), 'type error: ' + str(type(df)) + ' != pandas.core.frame.DataFrame'
    return (df - df.mean()) / (df.max() - df.min())


def sim_distance(sensor1, sensor2):
    '''
    ユークリッド距離によるスコアを計算する

    '''
    assert isinstance(sensor1, np.ndarray), 'type error: ' + str(type(sensor1)) + ' != numpy.ndarray'
    assert isinstance(sensor2, np.ndarray), 'type error: ' + str(type(sensor2)) + ' != numpy.ndarray'
    assert len(sensor1) == len(sensor2), 'sensor1 and sensor2 must be the same length'
    
    diff_sensor = sensor1 - sensor2
    sum_of_squares = sum([x**2 for x in diff_sensor])
    
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson():
    '''
    ピアソン相関によるスコアを計算する

    値が違うが傾向が同じときに近くなる方法
    センサ値に使用するのは適切ではない気がする
    '''
    return "TODO"
    

def sim_cos(sensor1, sensor2):
    '''
    コサイン類似度
    ベクトルx,yのなす角θの余弦cosθをコサイン類似度といい，
    ベクトルの向きの近さを類似性の指標としたもの
    ベクトルの向きが一致している時，最大値の１をとり，
    直交ならば0，向きが逆ならば最小値の-1をとる
    sim= x・y /(|x|*|y|)
     x・y <- 内積
    |x| <- xの長さ
    |y| <- yの長さ
    '''
    return sum(sensor1 * sensor2) / np.linalg.norm(sensor1) * np.linalg.norm(sensor2)



def top_matches(records,current,n=100,similarity=sim_cos):
    '''
    現在のセンサ値との類似度で過去のセンサログをランキングし上位n件を返す

    '''
    assert isinstance(records, pd.core.frame.DataFrame), 'type error: ' + str(type(records)) + ' != pandas.core.frame.DataFrame'
    assert isinstance(current, np.ndarray), 'type error: ' + str(type(current)) + ' != numpy.ndarray'

    # Score計算
    scores = [similarity(record, current) for record in records.values]

    # Scoreとタイムスタンプを紐づけるためにScore配列をSeries化
    scores_series = pd.Series(scores, index=records.index)

    # sortして上位n件を返す
    return scores_series.order(ascending=False).ix[0:n]


def predict_appliance_status(sensors, appliances, current):
    '''
    現在のセンサログ値に近いログ100件から現在の家電の状態を予測したスコアを計算する
    1.現在のセンサログの値に近い過去のセンサログの類似度スコア100件を取得
    2.その全てについてその時点の家電状態とスコアを掛け合わしたものを合計する
    3.正規化のためにスコアの合計値で割る

    '''
    assert isinstance(sensors, pd.core.frame.DataFrame), 'type error: ' + str(type(sensors)) + ' != pandas.core.frame.DataFrame'
    assert isinstance(appliances, pd.core.frame.DataFrame), 'type error: ' + str(type(appliances)) + ' != pandas.core.frame.DataFrame'    
    assert len(appliances) == len(sensors), 'sensors and appliances must be the same length'
    if not isinstance(current, np.ndarray) and isinstance(current, list):
        current_sensor = np.array(current).astype(float)

    # 現在のセンサデータに最も近い過去のセンサデータ上位100件の類似度スコアを取得
    sensor_scores = top_matches(normalize(sensors), current)

    # タイムスタンプだけ切り出し
    timestamp = sensor_scores.index

    appliance_score = np.zeros(len(appliances.axes[1])) # 家電の数の長さの配列を用意し0でうめる

    # 家電状態とその時点のセンサ値の類似度スコアをかけたものを100件合計    
    for t in timestamp:
        appliance_score += np.array([sensor_scores.ix[t] * x for x in appliances.ix[t]]) 
        
    # スコアの合計を計算
    sum_score = sensor_scores.sum()

    # 正規化
    result = appliance_score / sum_score

    return result


def recommend(sensors, appliances, current_sensor, current_appliance, on_threshold=0.8, off_threshold=0.2):
    '''
    家電操作推薦
    現在の家電状態と予測した家電状態のずれが閾値を超えた場合に家電操作を推薦する

    '''
    if not isinstance(current_sensor, np.ndarray) and isinstance(current_sensor, list):
        current_sensor = np.array(current_sensor).astype(float)
    
    status_diff = predict_appliance_status(sensors, appliances, current_sensor) - current_appliance
    status = [score_to_status(x, on_threshold, off_threshold) for x in status_diff]
    result = []
    
    for i in range(len(status)):
        if status[i] != 0:
            result.append((appliances.columns.values[i], status[i]))

    return result


def score_to_status(score, on_threshold, off_threshold):
    '''
    家電の状態予測スコアと現在の家電の状態を使って推薦すべき状態に変換する
    '''
    if score >= on_threshold:
        return 'on'
    elif score <= off_threshold - 1:
        return 'off'
    else:
        return 0
    
    

