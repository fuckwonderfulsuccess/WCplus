# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: instance\__init__.py
"""
定义全局对象
"""
from cmp.db.mongo import CollectionOperation
col_crawler_log = CollectionOperation('crawler_log')
col_req_data = CollectionOperation('req_data')
from app.weixin_crawler.req_data import ReqData
rd = ReqData()
from app.api.settings import Settings
user_settings = Settings()
from app.weixin_crawler import Stop
stop_and_start = Stop()
from utils.base import the_platform
PLATFORM = the_platform()