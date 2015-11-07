#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser_base

class ApplianceParserModule(parser_base.ParserModule):

    def __init__(self, bind_addr):
        super().__init__(bind_addr, ApplianceParser())

    def setup(self):
        super().setup('appliance')

    def run(self):
        super().run()

    def stop(self):
        super().stop()


class ApplianceParser(parser_base.Parser):
        
    def parse(self, data):
        return [('appliance', '{"light": 0}'), ('appliance', '{"viera": 1}')]


if __name__ == "__main__":
    proc = ApplianceParserModule('127.0.0.1:5558')
    proc.run()
        
