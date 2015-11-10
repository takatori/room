#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tornado.options import define, options
from room.output.output import OutputModule, Action

define("action_input_addr", default='127.0.0.1:5555')

class DefaultOutputModule(OutputModule):

    def __init__(self, bind_addr):
        super().__init__(bind_addr, DefaultAction())
        
    def setup(self):
        super().setup('')
        
class DefaultAction(Action):

    def action(self, data):
        print(data)

if __name__ == '__main__':
    proc = DefaultOutputModule(options.action_input_addr)
    proc.run()
