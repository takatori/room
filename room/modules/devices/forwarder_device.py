#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
from room.utils import log

class Forwarder(object):

    def __init__(self, front_port, backend_port):
        self._front_port = front_port
        self._backend_port = backend_port
        self._context = None
        self._frontend = None
        self._backend = None
        
    def main(self):

        try:
            self._context = zmq.Context(1)
            # Socket facing clients
            self._frontend = self._context.socket(zmq.SUB)
            self._frontend.bind("tcp://*:%s" % self._front_port)

            self._frontend.setsockopt(zmq.SUBSCRIBE, b"")

            # Socket facing services
            self._backend = self._context.socket(zmq.PUB)
            self._backend.bind("tcp://*:%s" %  self._backend_port)

            log.logging.info("Start forwarding from %s to %s", self._front_port, self._backend_port)
            zmq.device(zmq.FORWARDER, self._frontend, self._backend)

        except Exception as e:
            print(e)
            log.logging.error(e)
            print("bringing down zmq device")
            
        finally:
            pass
            self._frontend.close()
            self._backend.close()
            self._context.term()


    

