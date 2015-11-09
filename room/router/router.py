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
from tornado.options import define, options, parse_command_line
from zmq.utils import jsonapi as json

from room.utils.publisher import Publisher

define("port", default=8888, help="run on the given port", type=int)
define("output_addr", default="127.0.0.1:5558")
define("debug", default=False, help="run in debug mode")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Front")

class DataHandler(tornado.web.RequestHandler):
    '''
    データ受け取り口
    JSONデータを受け取る
    format `` { "data-type": "sparkcore", "data": {...} } ``

    '''
    def __init__(self):
        publisher = Publisher(options.output_addr)
    
    def post(self):
        data = json.loads(self.request.body.decode('utf-8')) # jsonデータが投げられると断定
        data_type = data.pop('data-type')  # parserの種類
        publisher.send(data_type, 'parse', data)
        self.write(data)

class Application(object):

    def __init__(self):
        self._loop = tornado.ioloop.IOLoop.current()
        app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/data", DataHandler),
            ],
            debug=options.debug,
        )
        app.listen(options.port)

    def start(self):
        print("Start app!")
        self._loop.start()
        
    def stop(self):
        print("Stop app!")    
        self._loop.stop()
        
if __name__ == "__main__":
    app = Application()
    app.start()


