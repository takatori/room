#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import parser
from room.utils.config import config

class ApplianceParserModule(parser.ParserModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(config['router_parser_forwarder']['back_port']),
            send_addr=int(config['parser_buffer_forwarder']['front_port']),
            recv_title='appliance_status',
            send_title='',
            category='appliance',
            parser=ApplianceParser()
        )

class ApplianceParser(parser.Parser):
        
    def parse(self, data):
        data.pop('time')
        return [{key: data[key]} for key in data.keys()]

    
if __name__ == "__main__":
    process = ApplianceParserModule()
    process.run()
        
