#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.modules.devices.forwarder_device import Forwarder
from room.utils.config import config

def main():
    router_parser_forwarder = Forwarder(config['router_parser_forwarder']['front_port'],
                                        config['router_parser_forwarder']['back_port'])
    router_parser_forwarder.main()

if __name__ == '__main__':
    main()


