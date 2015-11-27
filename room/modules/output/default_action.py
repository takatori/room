#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from room.output.output import OutputModule, Action
from room.utils.config import config


class DefaultOutputModule(OutputModule):

    def __init__(self, port):
        super().__init__('localhost:{0}'.format(port), DefaultAction())
        
    def setup(self):
        super().setup('')
        
class DefaultAction(Action):

    def action(self, data):
        print(data)

if __name__ == '__main__':
    proc = DefaultOutputModule(config['core_output_forwarder']['back_port'])
    proc.run()
