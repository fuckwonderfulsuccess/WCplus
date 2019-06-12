# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\search\search.py
"""
即用即创建 不永久驻留在内存中 专门为公众号数据搜索建立的类 主要完成如下几项工作
输入：搜索关键词（含有搜索规则） 搜索字段范围 公众号（index）范围
输入来来自前端返回的数据
每次搜索都创建一个对象
"""
from cmp.db.es.search import l1lll11lll_wcplus_

class l1ll111l1_wcplus_:

    def __init__(self, l1lll1l11l_wcplus_, l1l1l1lll_wcplus_='*', _1lll1l1l1_wcplus_=0, _1lll11ll1_wcplus_=10, fields=['title', 'article', 'digest']):
        """
        :param search_data: 带有搜索规则的关键字
        :param gzhs: 搜索的公众号范围列表
        :param in_range: 搜索的字段
        :param _from: 结果起始
        :param _size: 返回的数量
        :param fields: 搜索的范围
        """
        self.l1lll1l11l_wcplus_ = l1lll1l11l_wcplus_
        self.l1l1l1lll_wcplus_ = l1l1l1lll_wcplus_
        self.fields = fields
        self.l1lll1l1ll_wcplus_ = {'from':_1lll1l1l1_wcplus_,  'size':_1lll11ll1_wcplus_}

    def get_result(self):
        """
        :return: 根据参数设定返回搜索结果
        """
        s = l1lll11lll_wcplus_(l1lll1l11l_wcplus_=self.l1lll1l11l_wcplus_, index_list=self.l1l1l1lll_wcplus_, fields=self.fields, l1lll1l1ll_wcplus_=self.l1lll1l1ll_wcplus_)
        return s.search()

    @staticmethod
    def l1l1l1ll1_wcplus_():
        """
        :return: 获取es中可用索引
        """
        from app.search.index import l1l1lll1l_wcplus_
        from cmp.db.es.index import l1l1ll111_wcplus_
        index_list = l1l1lll1l_wcplus_.l1llll1111_wcplus_('gzh_*')
        l11l11lll_wcplus_ = []
        for index in index_list:
            l1lll1l111_wcplus_ = index.split('_')[-1]
            l1lll1ll11_wcplus_ = (l1l1ll111_wcplus_(index, doc_type='gzh_article')).count()
            l11l11lll_wcplus_.append([l1lll1l111_wcplus_, l1lll1ll11_wcplus_])

        return l11l11lll_wcplus_


if __name__ == '__main__':
    data = l1ll111l1_wcplus_.l1l1l1ll1_wcplus_()
    print(data)