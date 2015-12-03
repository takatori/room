#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zmq
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import time
from tornado.concurrent import Future
from tornado import gen
from zmq.utils import jsonapi as json

from room.publisher import Publisher
from room.utils import log
from room.utils.config import config
from room.utils.config import network_config

publisher = Publisher(int(network_config['forwarder1']['front']))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DataHandler(tornado.web.RequestHandler):
    '''
    データ受け取り口
    JSONデータを受け取る
    format `` { "data-type": "sparkcore", "data": {...} } ``

    '''
    def post(self):
        data = json.loads(self.request.body.decode('utf-8')) # jsonデータが投げられると断定
        log.logging.info(data)
        parser_name = data.pop('data_type')
        publisher.send(data['data'], title=parser_name)
        self.write(data)
    

class Application(object):
    '''
    Webアプリケーション設定

    '''
    def __init__(self):
        app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/data", DataHandler),
            ],
            debug=config['server']['debug'],
            template_path=os.path.join(os.getcwd(),  "templates"),
            static_path=os.path.join(os.getcwd(),  "static"),            
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


