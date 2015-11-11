#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import time

from tornado.concurrent import Future
from tornado import gen
from zmq.utils import jsonapi as json

from room.utils.publisher import Publisher
from room.utils import log
from room.utils.config import config

publisher = Publisher(config['router_parser_forwarder']['front_port'])

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Front")

class DataHandler(tornado.web.RequestHandler):
    '''
    データ受け取り口
    JSONデータを受け取る
    format `` { "data-type": "sparkcore", "data": {...} } ``

    '''
    def post(self):
        data = json.loads(self.request.body.decode('utf-8')) # jsonデータが投げられると断定
        log.logging.info(data)
        data_type = data.pop('data-type')  # parserの種類
        publisher.send(data_type, 'parse', data['data'])
        self.write(data)
    
class Application(object):

    def __init__(self):
        app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/data", DataHandler),
            ],
            debug=config['server']['debug'],
        )
        app.listen(config['server']['port'])
        self._loop = tornado.ioloop.IOLoop.current()        

    def start(self):
        print("Start app!")
        self._loop.start()
        
    def stop(self):
        print("Stop app!")    
        self._loop.stop()

if __name__ == "__main__":
    app = Application()
    app.start()


