#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json

from room.parser.sparkcore_parser import SparkCoreParser

class SparkCoreParserTest(unittest.TestCase):

    def test_parser(self):
        parser = SparkCoreParser()
        data = """
        ["sparkcore",{
        "sensorId": "core04",
        "temperature": 27.6,
        "humidity": 41.200001,
        "pressure": 991.455566,
        "brightness": 34.848484,
        "pir_count": 0
        }]"""
        results = parser.parse(json.loads(data))
        expections = ['{"core04_temperature": 27.6}',
                      '{"core04_humidity": 41.200001}',
                      '{"core04_pressure": 991.455566}',
                      '{"core04_brightness": 34.848484}',
                      '{"core04_pir_count": 0}']
        for result in results:
            self.assertEqual(result[0], 'sensor')
            self.assertTrue(result[1] in expections)


        
if __name__ == '__main__':
    unittest.main()        

