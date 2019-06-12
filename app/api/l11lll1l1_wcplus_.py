# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\l11lll1l1_wcplus_.py
"""
为已经采集的公众号页面提供数据支持
"""
from instance import l1l1l11l1_wcplus_
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
from utils.base import l1lll1111_wcplus_
from utils.l11ll1111_wcplus_ import l11llll11_wcplus_

class l11ll1l1l_wcplus_:

    def __init__(self):
        pass

    def get(self):
        """
        :return:获取所有公众号列表
        """
        l11lll111_wcplus_ = []
        l11lll1ll_wcplus_ = 0
        l11ll11l1_wcplus_ = 0
        l1l1l1lll_wcplus_ = l1l1l11l1_wcplus_.get()
        cnt = 1
        for i in l1l1l1lll_wcplus_:
            l11lll1ll_wcplus_ += 1
            l11ll111l_wcplus_ = l1l11llll_wcplus_(i['nickname'])
            l11ll1lll_wcplus_ = {}
            l11ll1l11_wcplus_ = l11ll111l_wcplus_.count()
            l11ll11l1_wcplus_ += l11ll1l11_wcplus_
            l11ll11ll_wcplus_ = l11ll111l_wcplus_.count(read_num={'$gt': -2})
            l11ll1lll_wcplus_['id'] = cnt
            l11ll1lll_wcplus_['nickname'] = i['nickname']
            l11ll1lll_wcplus_['total_articles'] = l11ll1l11_wcplus_
            l11ll1lll_wcplus_['reading_data_articles'] = l11ll11ll_wcplus_
            l11ll1lll_wcplus_['time'] = i['time'].timestamp()
            cnt += 1
            l11lll111_wcplus_.append(l11ll1lll_wcplus_)

        return {'finished':l11lll111_wcplus_,  'stat_data':{'gzh_num':l11lll1ll_wcplus_,  'article_num':l11ll11l1_wcplus_}}

    def l11ll1ll1_wcplus_(self, l11l1llll_wcplus_):
        """
        :param page_info: {'nickname','start','end'}
        :return: 返回一个公众号的全部文章列表
        """
        from pymongo import DESCENDING
        l11ll111l_wcplus_ = l1l11llll_wcplus_(l11l1llll_wcplus_['nickname'])
        l11lll111_wcplus_ = []
        cnt = 1
        l11lll11l_wcplus_ = l11ll111l_wcplus_.table.find().sort('p_date', DESCENDING)[int(l11l1llll_wcplus_['start']):int(l11l1llll_wcplus_['end'])]
        for a in l11lll11l_wcplus_:
            item = {}
            item['id'] = cnt
            item['mov'] = str(a['mov'])
            if 'read_num' in a:
                item['read'] = a['read_num']
            else:
                item['read'] = '-'
            if 'like_num' in a:
                item['like'] = a['like_num']
            else:
                item['like'] = '-'
            if 'reward_num' in a:
                item['reward'] = a['reward_num']
            else:
                item['reward'] = '-'
            if 'comment_num' in a:
                item['comment'] = a['comment_num']
            else:
                item['comment'] = '-'
            item['date'] = a['p_date'].timestamp()
            item['title'] = a['title']
            item['url'] = a['content_url']
            item['md5'] = l11llll11_wcplus_(a['content_url'])
            cnt += 1
            l11lll111_wcplus_.append(item)

        return l11lll111_wcplus_