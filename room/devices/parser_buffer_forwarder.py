#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.devices.forwarder_device import Forwarder
from room.utils.config import config


def main():
    parser_buffer_forwarder = Forwarder(config['parser_buffer_forwarder']['front_port'],
                                        config['parser_buffer_forwarder']['back_port'])
    parser_buffer_forwarder.main()

if __name__ == '__main__':
    main()
