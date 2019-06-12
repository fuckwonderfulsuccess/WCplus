# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: l1l11_wcplus_\api\search.py
from flask_restful import Resource, reqparse
parser = reqparse.RequestParser()
arguments = [
 'range', 'search_data', 'fields', 'from', 'size']
for arg in arguments:
    parser.add_argument(arg)

class l1lll11lll_wcplus_(Resource):

    def get(self):
        """
        :return: 打开搜索页 返回可用的搜索信息
        """
        from app.api.search import l11l11lll_wcplus_
        return l11l11lll_wcplus_()

    def post(self):
        """
        :return: 返回搜索的结果
        1标题 2摘要 3文章 4全部
        """
        args = parser.parse_args()
        if args['fields'] == '1':
            args['fields'] = [
             'title']
        else:
            if args['fields'] == '2':
                args['fields'] = [
                 'digest']
            else:
                if args['fields'] == '3':
                    args['fields'] = [
                     'article']
                else:
                    args['fields'] = [
                     'title', 'digest', 'article']
        if args['range'] == '全部':
            args['range'] = 'gzh_*'
        else:
            args['range'] = 'gzh_' + args['range']
        from app.search.search import l1ll111l1_wcplus_
        try:
            result = (l1ll111l1_wcplus_(l1lll1l11l_wcplus_=args['search_data'], l1l1l1lll_wcplus_=args['range'],
              fields=args['fields'],
              _1lll1l1l1_wcplus_=int(args['from']),
              _1lll11ll1_wcplus_=int(args['size']))).get_result()
            return result
        except:
            from utils.base import logger
            logger.warning('搜索请求超时 建议多次尝试')
            return '搜索请求超时 建议多次尝试'