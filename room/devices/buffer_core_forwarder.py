#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.devices.forwarder_device import Forwarder
from room.utils.config import config

def main():
    buffer_core_forwarder   = Forwarder(config['buffer_core_forwarder']['front_port'],
                                        config['buffer_core_forwarder']['back_port'])
    buffer_core_forwarder.main()

if __name__ == '__main__':
    main()

    
