# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\search\index.py
"""
文章建立索引的情况
1. 采集阶段 第一次采集完成
2. 采集阶段 更新采集过的公众号
1 处理流程：
0: 先检查该公众号是否存在索引如果索引存在计算文章的数量 以此判断到底应该准备多少公众号的文章
a：从数据库中读取出该公众号的全部数据
b：冲html文件夹中读取所有的html文档 解析成为内容文本
c：解析出html中的文本，组成完整的文章数据
d：数据写入es es根据id跳过已经存在的文档
2 处理流程
处理逻辑和1 一样遇到更新就直接跳出
更新的几种情况
1. 阅读数据更新
2. 文章内容从无到有
索引发生在什么情况下？
情况1 一个公众号采集完毕之后，需要准备索引的速度足够快 创建GZHIndex对象 调用index方法
情况2 一个公众号的数据更新之后，需要准备索引数据的速度足够快 创建GZHIndex对象 调用index方法
情况3 对于3.0 已经采集的数据建立索引 先将html文档解析成文本放入数据库 再调用 index方法
"""
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
from app.search.config import l1llll1lll_wcplus_
from utils.base import logger
from cmp.db.es.index import l1l1ll111_wcplus_
import time

class l1l1lll1l_wcplus_:
    l1llll11ll_wcplus_ = 'gzh_'
    doc_type = 'gzh_article'

    def __init__(self, nickname):
        self.nickname = nickname.lower()
        self.l1lll1lll1_wcplus_ = nickname

    def l1llll111l_wcplus_(self):
        """
        :return: 检查该index是否存在
        """
        return l1l1ll111_wcplus_.l1lll1llll_wcplus_(self.nickname)

    @staticmethod
    def l1llll1111_wcplus_(l1lll1ll1l_wcplus_=None):
        """
        :param patton: 支持通配符
        :return: 所有加入index的文档和文档数量
        """
        return l1l1ll111_wcplus_.l1llll1111_wcplus_(l1lll1ll1l_wcplus_)

    def l1llll1l1l_wcplus_(self, num=None):
        """
        :param num: 如果是具体数字则 准备最近发布的num篇文章
        :return: 根据公众号的昵称准备该公众号的所有或者前n篇文章的全部数据 如果某些字段没有就使用默认值
        """
        from pymongo import DESCENDING
        l1llll1l11_wcplus_ = []
        col = l1l11llll_wcplus_(self.l1lll1lll1_wcplus_)
        if num:
            l11111l1l_wcplus_ = col.table.find().sort('p_date', DESCENDING)()[:num]
        else:
            l11111l1l_wcplus_ = col.get()
        begin_time = time.time()
        for doc in l11111l1l_wcplus_:
            item = {}
            doc['id'] = doc['content_url']
            for key in l1llll1lll_wcplus_:
                if key in doc:
                    item[key] = doc[key]
                else:
                    item[key] = -2

            l1llll1l11_wcplus_.append(item)

        logger.info('解析文章文本用时 %.3f' % (time.time() - begin_time))
        return l1llll1l11_wcplus_

    def index(self, num=None):
        """
        :param num: 需要冲数据库中挑选出的文章数量
        :return: 用最有效率的方式将文档index到es中
        如果index_check之后的结果和数据库中的文档数量一致 直接跳过 不index
        如果数据和结果不一样 全文再次更新索引
        """
        l1llll1l11_wcplus_ = self.l1llll1l1l_wcplus_(num=num)
        index_doc = l1l1ll111_wcplus_(self.l1llll11ll_wcplus_ + self.nickname, l1llll1l11_wcplus_, self.doc_type)
        index_doc.create_index()
        index_doc.l1llll11l1_wcplus_()

    def delete(self):
        """
        :return: 删除该index
        """
        l1l1ll111_wcplus_.l1l1lll11_wcplus_(self.l1llll11ll_wcplus_ + self.nickname)