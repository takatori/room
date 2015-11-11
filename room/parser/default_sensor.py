#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from room.parser import parser_base
from room.utils.config import config

class DefaultSensorParserModule(parser_base.ParserModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), DefaultSensorParser())


    def setup(self):
        super().setup('default_sensor')


class DefaultSensorParser(parser_base.Parser):

    def parse(self, data):
        data = data[1]
        return [('sensor', {key: data[key]}) for key in data.keys()]

if __name__ == "__main__":
    proc = DefaultSensorParserModule(config['router_parser_forwarder']['back_port'])
    proc.run()
        

