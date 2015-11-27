#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.output import OutputModule, Action
from room.utils.config import config

class StdOutModule(OutputModule):

    def __init__(self, port):
        super().__init__(
            recv_addr='localhost:{0}'.format(config['core_output_forwarder']['back_port']),
            recv_title='',
            action=StdOut()
        )

class StdOut(Action):

    def action(self, data):
        print(data)

if __name__ == '__main__':
    process = StdOutModule()
    process.run()
