# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: l1l11_wcplus_\api\l1lll1_wcplus_.py
from flask_restful import Resource, reqparse
parser = reqparse.RequestParser()
arguments = ['range', 'type', 'num', 'start_time', 'end_time', 'nick_name', 'article_location']
for arg in arguments:
    parser.add_argument(arg)

class l11lll1l1l_wcplus_(Resource):

    def get(self):
        pass

    def post(self):
        from app.api.l1lll1_wcplus_ import l1l111l1l_wcplus_
        from threading import Thread
        args = parser.parse_args()
        (Thread(target=l1l111l1l_wcplus_(args).l1l11l1ll_wcplus_)).start()

    def delete(self):
        from instance import rd
        l11l1l111l_wcplus_ = parser.parse_args()['nick_name']
        rd.delete(l11l1l111l_wcplus_)