#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
from  multiprocessing import Process

from room.utils import log
from room.utils.config import network_config

def forward(front_port, backend_port):

    context = zmq.Context(1)
    # Socket facing clients
    frontend = context.socket(zmq.SUB)
    frontend.bind("tcp://*:%s" % front_port)

    frontend.setsockopt(zmq.SUBSCRIBE, b"")

    # Socket facing services
    backend = context.socket(zmq.PUB)
    backend.bind("tcp://*:%s" % backend_port)
    
    try:
        log.logging.info("Start forwarding from %s to %s", front_port, backend_port)
        zmq.device(zmq.FORWARDER, frontend, backend)
        
    except Exception as e:
        print(e)
        log.logging.error(e)
        print("bringing down zmq device")
            
    finally:
        frontend.close()
        backend.close()
        context.term()

    
if __name__ == '__main__':

    for section in network_config.sections():
        front_port = int(network_config[section]['front'])
        back_port  = int(network_config[section]['back'])
        Process(target=forward, args=(front_port, back_port,)).start()

