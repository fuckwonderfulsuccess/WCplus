# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: l1l11_wcplus_\__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api
from flask_cors import CORS
import logging
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
l1ll11l11ll_wcplus_ = Flask('WCplus', template_folder='./web_server/static', static_folder='./web_server/static')
CORS(l1ll11l11ll_wcplus_, resources={'/api/*': {'origins': '*'}})
from l1l11_wcplus_.api import l1ll11l1ll1_wcplus_
api = Api(l1ll11l11ll_wcplus_)
for item in l1ll11l1ll1_wcplus_:
    api.add_resource(item['res'], '/api' + item['url'])

socketio = None
from instance import l1_wcplus_
if l1_wcplus_ == 'osx':
    socketio = SocketIO(l1ll11l11ll_wcplus_, l1ll11ll1ll_wcplus_=False)
else:
    if l1_wcplus_ == 'win':
        try:
            socketio = SocketIO(l1ll11l11ll_wcplus_, async_mode='gevent', l1ll11ll1ll_wcplus_=False)
        except:
            socketio = SocketIO(l1ll11l11ll_wcplus_, l1ll11ll1ll_wcplus_=False)

        from l1l11_wcplus_.router import *
        from l1l11_wcplus_.event import *

        def l1ll1l_wcplus_():
            socketio.run(l1ll11l11ll_wcplus_, host='0.0.0.0', port=5000)