#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from room.devices.forwarder_device import Forwarder
from room.utils.config import config

def main():
    core_output_forwarder   = Forwarder(config['core_output_forwarder']['front_port'],
                                        config['core_output_forwarder']['back_port'])
    core_output_forwarder.main()

if __name__ == '__main__':
    main()


