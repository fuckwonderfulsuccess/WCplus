# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: web_server\api\__init__.py
"""
RESTful API
"""
from web_server.api.helloworld import HelloWorld
from web_server.api.crawler import Crawler
from web_server.api.gzh import GZH
from web_server.api.settings import Settings
api_resources = [
 {'res':HelloWorld, 
  'url':'/helloworld'},
 {'res':Crawler, 
  'url':'/crawler'},
 {'res':GZH, 
  'url':'/gzh'},
 {'res':Settings, 
  'url':'/settings'}]