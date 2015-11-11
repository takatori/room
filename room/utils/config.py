# -*- coding: utf-8 -*-

import os
import configparser

config = configparser.ConfigParser()
config.read(os.environ['PYTHONPATH'] + '/config.ini')

