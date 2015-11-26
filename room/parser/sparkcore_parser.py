#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from room.parser import parser_base
from room.utils.config import config

class SparkCoreParserModule(parser_base.ParserModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), SparkCoreParser())

    def setup(self):
        super().setup('sparkcore')

class SparkCoreParser(parser_base.Parser):
        
    def parse(self, data):
        data.pop('time')
        coreId = data.pop('sensorId')
        return [('sensor', json.dumps({coreId + "_" + key: data[key]}))
            for key in data.keys()]

if __name__ == "__main__":
    proc = SparkCoreParserModule(config['router_parser_forwarder']['back_port'])
    proc.run()
        
