#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser_base

from room.utils.config import config

class ApplianceParserModule(parser_base.ParserModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), ApplianceParser())

    def setup(self):
        super().setup('appliance')

class ApplianceParser(parser_base.Parser):
        
    def parse(self, data):
        return [('appliance', {key: data[key]}) for key in data.keys()]


if __name__ == "__main__":
    proc = ApplianceParserModule(config['router_parser_forwarder']['back_port'])
    proc.run()
        
