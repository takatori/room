#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import random
import csv

def sensorlog():
    return list(csv.reader(open('../output/sensor.csv')))[1:]

def sparkcorelog():
    reader0 = csv.reader(open('../output/core00.csv'))
    reader1 = csv.reader(open('../output/core01.csv'))
    reader2 = csv.reader(open('../output/core02.csv'))
    reader4 = csv.reader(open('../output/core04.csv'))

    readers = [reader0, reader1, reader2, reader4]
    return [list(reader) for reader in readers]

def appliancelog():
    return list(csv.reader(open('../output/appliancelog.csv')))[1:]

def appliance_statuslog():    
    return list(csv.reader(open('../output/status.csv')))[1:]
    
    
