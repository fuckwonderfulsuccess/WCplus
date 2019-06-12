# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\es\search.py
"""
作为搜索模块 应该提供哪些功能
执行一次搜索创建一个对象
"""
import re
from cmp.db.es.config import search_template
from copy import deepcopy
from cmp.db.es import l11l111ll1_wcplus_
from utils.base import logger, l1lll1111_wcplus_

class l1lll11lll_wcplus_:

    def __init__(self, l1lll1l11l_wcplus_, index_list, l1lll1l1ll_wcplus_={'from':0, 
 'size':10}, fields=['title', 'article', 'author', 'digest', 'comments'], doc_type='gzh_article', source=None):
        """
        :param index_list: 所需要搜搜的索引列表
        :param search_words: 搜索关键字 支持通配符
        """
        self.index_list = index_list
        self.l1lll1l11l_wcplus_ = l1lll1l11l_wcplus_
        self.doc_type = doc_type
        self.l111ll1ll1_wcplus_ = fields
        self.l1lll1l1ll_wcplus_ = l1lll1l1ll_wcplus_
        self.source = source

    def search(self):
        """
        :return: 执行搜索动作
        """
        indices = []
        st = deepcopy(search_template)
        l111ll11l1_wcplus_ = self.l11l1111ll_wcplus_()
        st.update(l111ll11l1_wcplus_)
        if self.source != None:
            st['_source'] = self.source
        try:
            st['from'] = self.l1lll1l1ll_wcplus_['from']
            st['size'] = self.l1lll1l1ll_wcplus_['size']
        except:
            logger.warning('from_size字段错误 %s' % str(self.l1lll1l1ll_wcplus_))

        if not self.index_list:
            indices = '*'
        else:
            indices = self.index_list
        try:
            result = (l11l111ll1_wcplus_.search(index=indices, doc_type=self.doc_type, body=st))['hits']
            return result
        except Exception as e:
            print(e)
            logger.error('搜索错误 可能是有指定了不存在的搜索范围没有建立索引%s' % str(indices))
            return False

    def l11l1111ll_wcplus_(self):
        """
        :return: 预处理搜索关键字 分理出其中的搜索模式
        :param search_data:
        :return: 对即将搜索的数据进行预处理 解析搜索模式
        数据中包含模式：
        双引号包含的内容使用match_phrase全匹配,双引号之外的内容使用分词模式match
        排序模式 指定排序字段以及升降方式
        举例："必须包含词"分词模式-time-1
        根据搜索数据中指定的规则返回查询的query、sort等字段数据
        """
        l111ll11ll_wcplus_ = {'loc':'mov', 
         'author':'author', 
         'time':'p_date', 
         'comm':'comments', 
         'reward':'reward_num', 
         'unk':'_score'}
        l111ll1l11_wcplus_ = {'0':'asc', 
         '1':'desc'}
        if len(re.findall('-', self.l1lll1l11l_wcplus_)) == 2:
            l111lll11l_wcplus_ = self.l1lll1l11l_wcplus_.split('-')
            try:
                l111llll11_wcplus_ = l111ll1l11_wcplus_[l111lll11l_wcplus_[-1]]
                l11l1111l1_wcplus_ = l111ll11ll_wcplus_[l111lll11l_wcplus_[-2]]
            except:
                l111llll11_wcplus_ = l111ll1l11_wcplus_['1']
                l11l1111l1_wcplus_ = l111ll11ll_wcplus_['unk']

        else:
            l111llll11_wcplus_ = l111ll1l11_wcplus_['1']
            l11l1111l1_wcplus_ = l111ll11ll_wcplus_['unk']
        l1lll1l11l_wcplus_ = self.l1lll1l11l_wcplus_.split('-')[0]
        l11l111111_wcplus_ = [x.replace('"', '') for x in re.findall('"\\S*?"', l1lll1l11l_wcplus_)]
        l111llll1l_wcplus_ = l1lll1l11l_wcplus_.replace('"', '')
        for x in l11l111111_wcplus_:
            l111llll1l_wcplus_ = l111llll1l_wcplus_.replace(x, '').replace(' ', '')

        l111llllll_wcplus_ = {'bool': {'should': []}}
        l111lllll1_wcplus_ = {'match_phrase': {}}
        l111ll1l1l_wcplus_ = {'match': {}}
        for f in self.l111ll1ll1_wcplus_:
            if l111llll1l_wcplus_ != '':
                l111lll1l1_wcplus_ = deepcopy(l111ll1l1l_wcplus_)
                l111lll1l1_wcplus_['match'][f] = l111llll1l_wcplus_
                l111llllll_wcplus_['bool']['should'].append(l111lll1l1_wcplus_)
            for item in l11l111111_wcplus_:
                l111lll1l1_wcplus_ = deepcopy(l111lllll1_wcplus_)
                l111lll1l1_wcplus_['match_phrase'][f] = item
                l111llllll_wcplus_['bool']['should'].append(l111lll1l1_wcplus_)

        l111lll111_wcplus_ = [
         {l11l1111l1_wcplus_: {'order': l111llll11_wcplus_}}]
        return {'query':l111llllll_wcplus_, 
         'sort':l111lll111_wcplus_}


if __name__ == '__main__':
    from utils.base import l1lll1111_wcplus_
    s = l1lll11lll_wcplus_('教育', ['gzh_阿拉升学说'], 'gzh_article')
    data = s.search()
    l1lll1111_wcplus_(data)