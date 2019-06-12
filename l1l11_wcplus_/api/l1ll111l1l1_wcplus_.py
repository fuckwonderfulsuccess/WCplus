# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: l1l11_wcplus_\api\l1ll111l1l1_wcplus_.py
from flask_restful import Resource, reqparse
parser = reqparse.RequestParser()
arguments = ['name', 'age']
for arg in arguments:
    parser.add_argument(arg)

class l1ll111l1ll_wcplus_(Resource):

    def get(self):
        return {'name':'frank', 
         'age':18}

    def post(self):
        args = parser.parse_args()
        print(args)