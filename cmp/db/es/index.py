# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\es\index.py
"""
作为一个通用的index组件 应该是什么样的？
提供文档类型 和一个文档list就够了
index相当于table 文档相当于数据
每个文档一定要有一个id字段 建议使用文章的url
"""
from app.search.config import l1llll1lll_wcplus_
from cmp.db.es import l11l111ll1_wcplus_
from elasticsearch import helpers
from utils.base import logger

class l1l1ll111_wcplus_:

    def __init__(self, index_name, l1llll1l11_wcplus_=None, doc_type='articles'):
        """
        :param index_name: index的名称
        :param doc_list:文档列表
        """
        self.index_name = index_name
        self.docs = l1llll1l11_wcplus_
        self.doc_type = doc_type

    def create_index(self):
        """
        :return: 创建index 如果已经存在则不创建
        返回是创建还是已经存 create index 实际上是告诉 es 哪些需要索引 哪些不需要索引
        """
        l11l11l111_wcplus_ = {}
        l11l11l111_wcplus_['properties'] = l1llll1lll_wcplus_
        exists = l11l111ll1_wcplus_.indices.exists(self.index_name)
        if exists is False:
            l11l111ll1_wcplus_.indices.create(self.index_name)
            l11l111ll1_wcplus_.indices.put_mapping(index=self.index_name, doc_type=self.doc_type, body=l11l11l111_wcplus_)
            logger.debug('创建index %s 成功' % self.index_name)
        else:
            logger.debug('index %s 已经存在' % self.index_name)
        return exists

    @staticmethod
    def l1l1lll11_wcplus_(index_name):
        """
        :param:指定index的匹配模式 支持通配符* 通过list指定多个index
        :return:删除index和该index下的所有doc
        """
        l11l111ll1_wcplus_.indices.delete(index_name)

    @staticmethod
    def l1llll1111_wcplus_(l1lll1ll1l_wcplus_=None):
        """
        :param patton: 支持通配符 *
        :return:
        """
        index_list = []
        try:
            alias = l11l111ll1_wcplus_.indices.get_alias(l1lll1ll1l_wcplus_)
        except:
            alias = []

        for key in alias:
            index_list.append(key)

        return index_list

    @staticmethod
    def l1lll1llll_wcplus_(index_name):
        """
        :param index_name:
        :return: 检查index是否存在
        """
        return l11l111ll1_wcplus_.indices.exists(index_name)

    def l11l11l11l_wcplus_(self):
        """
        :return: 索引文档 使用bulk操作
        """
        pass

    def index_doc(self, doc):
        """
        :param doc:文档体
        :return:新建或者更新doc
        """
        l11l111lll_wcplus_ = dict(((key, doc[key]) for key in l1llll1lll_wcplus_))
        if self.l11l11l1l1_wcplus_(doc['id']) == 1:
            return
            try:
                l11l111ll1_wcplus_.index(index=self.index_name, doc_type=self.doc_type, id=doc['content_url'], body=l11l111lll_wcplus_)
            except:
                logger.error('index 文档失败 %s' % doc['title'])

    def l1llll11l1_wcplus_(self):
        """
        :param index_name: es中的index名称
        :return:使用bulk进行批量index API会根据指定的_id字段去重 而且支持更新 index文档建议优先使用该API
        用id跟踪一篇文章 其余字段变化都是跟新模式 id变化则插入新文档
        """
        actions = []
        for doc in self.docs:
            action = {'_index':self.index_name, 
             '_type':self.doc_type, 
             '_id':doc['id'], 
             '_source':doc}
            actions.append(action)

        result = helpers.bulk(l11l111ll1_wcplus_, actions)
        return result

    def l11l11l1l1_wcplus_(self, id):
        """
        :param id: 文档id 一般使用文章的url
        :return:文档存在返回1 文档不存在返回0
        """
        try:
            body = {'query': {'match_phrase': {'id': id}}}
            result = (l11l111ll1_wcplus_.count(index=self.index_name, doc_type=self.doc_type, body=body))['count']
        except:
            result = 0

        return result

    def delete_doc(self, id):
        """
        :param nickname:
        :param url:
        :return: 根据id删除文档
        """
        l11l111ll1_wcplus_.delete(index=self.index_name, doc_type=self.doc_type, id=id)

    def count(self):
        """
        :return: get index doc num
        """
        try:
            body = {'query': {'match_all': {}}}
            result = (l11l111ll1_wcplus_.count(index=self.index_name, doc_type=self.doc_type, body=body))['count']
        except Exception as e:
            result = 0

        return result


if __name__ == '__main__':
    index = l1l1ll111_wcplus_.l1llll1111_wcplus_()
    print(index)