# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\settings.py
"""
提供数据设置API
"""
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
l11l11ll1_wcplus_ = l1l11llll_wcplus_('settings')

class l11l111ll_wcplus_:

    def __int__(self):
        pass

    def get(self):
        """
        :return: 获取所有的设置字段{}
        """
        sd = l11l11ll1_wcplus_.get()
        l11l11l11_wcplus_ = {}
        for s in sd:
            l11l11l11_wcplus_[s['key']] = s['value']

        from cmp.protect import Passport
        from utils.network import l111lllll_wcplus_
        l11l11l11_wcplus_['uuid'] = Passport.l11l111l1_wcplus_()
        l11l11l1l_wcplus_ = Passport.l1l11l111_wcplus_()
        if not l11l11l1l_wcplus_:
            l11l11l11_wcplus_['passport'] = 0
        else:
            l11l11l11_wcplus_['passport'] = l11l11l1l_wcplus_
        l11l11l11_wcplus_['proxy_server'] = l111lllll_wcplus_()
        return l11l11l11_wcplus_

    def insert(self, l11l1111l_wcplus_):
        """
        :param settings_data_dict: settings数据本质上是一个字典
        :return: 插入或修改
        """
        l11l11111_wcplus_ = []
        for key in l11l1111l_wcplus_:
            item = {}
            item['key'] = key
            item['value'] = l11l1111l_wcplus_[key]
            l11l11111_wcplus_.append(item)

        l11l11ll1_wcplus_.insert('key', l11l11111_wcplus_)

    def delete(self, key, all=False):
        """
        :param key:准确的key
        :param all:
        :return:
        """
        if all:
            l11l11ll1_wcplus_.delete()
        else:
            l11l11ll1_wcplus_.delete(key=key)