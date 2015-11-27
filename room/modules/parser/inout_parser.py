#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import parser
from room.utils.config import config

class InOutParserModule(parser.ParserModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(config['router_parser_forwarder']['back_port']),
            send_addr=int(config['parser_buffer_forwarder']['front_port']),
            recv_title='inout',
            send_title='',
            category='sensor',
            parser=InOutParser()
        )

class InOutParser(parser.Parser):
        
    def parse(self, data):
        user = data['user']
        state = 1 if data['state'] == 'in' else 0
        return [{user: state}]

    
if __name__ == "__main__":
    process = InOutParserModule()
    process.run()


