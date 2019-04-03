# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: web_server\__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api
from flask_cors import CORS
import logging
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
web_app = Flask('WCplus', template_folder='./web_server/static', static_folder='./web_server/static')
CORS(web_app, resources={'/api/*': {'origins': '*'}})
from web_server.api import api_resources
api = Api(web_app)
for item in api_resources:
    api.add_resource(item['res'], '/api' + item['url'])

socketio = None
from instance import PLATFORM
if PLATFORM == 'osx':
    socketio = SocketIO(web_app, log_output=False)
else:
    if PLATFORM == 'win':
        socketio = SocketIO(web_app, async_mode='gevent', log_output=False)
from web_server.router import *
from web_server.event import *

def run_webserver():
    socketio.run(web_app, host='0.0.0.0', port=5000)