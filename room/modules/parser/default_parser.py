#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room import parser
from room.utils.config import config

class DefaultParserModule(parser.ParserModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(5000),
            send_addr=5001,
            recv_title='default',
            send_title='',
            parser=DefaultParser()
        )

class DefaultParser(parser.Parser):

    def parse(self, data):
        return data

    
if __name__ == "__main__":
    process = DefaultParserModule()
    process.run()

