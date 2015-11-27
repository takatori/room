#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser_base
import json

from room.utils.config import config

class InOutParserModule(parser_base.ParserModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), InOutParser())

    def setup(self):
        super().setup('inout')

class InOutParser(parser_base.Parser):
        
    def parse(self, data):
        user = data['user']
        state = 1 if data['state'] == 'in' else 0
        return [('sensor', json.dumps({user: state}))]

    
if __name__ == "__main__":
    proc = InOutParserModule(config['router_parser_forwarder']['back_port'])
    proc.run()


