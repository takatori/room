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

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

class Publisher(object):

    def __init__(self):
        context = zmq.Context()
        self._sock = context.socket(zmq.PUB)
        self._sock.bind("tcp://*:5558")

        print("Starting broadcast")
        print("Hit Ctrl-C to stop broadcasting.")
        print("Waiting so subscriber sockets can connect...")
        time.sleep(1.0) # slow join問題

    def send(self, data_type, data):
        msg = json.dumps(['parse', data['data']])
        self._sock.send_multipart([data_type.encode('utf-8'), msg])

publisher = Publisher()

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
        data_type = data.pop('data-type')  # parserの種類
        publisher.send(data_type, data) # parserを指定してデータを送信
        self.write(data)

def main():
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/data", DataHandler),
        ],
        debug=options.debug,
    )
    app.listen(options.port)
    print("Start app!")
    tornado.ioloop.IOLoop.current().start()    

if __name__ == "__main__":
    main()


