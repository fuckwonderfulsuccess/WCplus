# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: web_server\api\crawler.py
from flask_restful import Resource, reqparse
parser = reqparse.RequestParser()
arguments = ['range', 'type', 'num', 'start_time', 'end_time', 'nick_name']
for arg in arguments:
    parser.add_argument(arg)

class Crawler(Resource):

    def get(self):
        pass

    def post(self):
        from app.api.crawler import Begin2Crawl
        from threading import Thread
        args = parser.parse_args()
        (Thread(target=Begin2Crawl(args).crawl)).start()

    def delete(self):
        from instance import rd
        nick_name = parser.parse_args()['nick_name']
        rd.delete(nick_name)