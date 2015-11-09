#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from room.parser import parser_base

class SparkCoreParserModule(parser_base.ParserModule):

    def __init__(self, bind_addr):
        super().__init__(bind_addr, SparkCoreParser())

    def setup(self):
        super().setup('sparkcore')

    def run(self):
        super().run()

    def stop(self):
        super().stop()

class SparkCoreParser(parser_base.Parser):
        
    def parse(self, data):
        data = data[1]
        coreId = data.pop('sensorId')
        return [('sensor', json.dumps({coreId + "_" + key: data[key]}))
            for key in data.keys()]

if __name__ == "__main__":
    proc = SparkCoreParserModule('127.0.0.1:5558')
    proc.run()
        