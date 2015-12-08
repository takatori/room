# -*- coding: utf-8 -*-

import uuid
from tornado import gen
#from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from room.output import OutputModule, Action
from room.utils.config import config, network_config


class HttpOutputModule(OutputModule):

    def __init__(self):
        super().__init__(
            recv_addr='localhost:{0}'.format(network_config['forwarder5']['back']),            
            recv_title='',
            action=HttpOut()
        )

class HttpOut(Action):
    
    def action(self, data):
        http_client = AsyncHTTPClient()
        for appliance, method in data:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}            
            payload = {"recommend_id": str(uuid.uuid4()), "appliance": appliance, "method": method}
            request = HTTPRequest(config['http_output']['url'], 'POST', headers, body=data)
            response = yield http_client.fetch(request)
            print(response)
        

if __name__ == '__main__':
    process = HttpOutputModule()
    process.run()
