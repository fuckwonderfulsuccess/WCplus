# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\l1ll11l11_wcplus_\__init__.py
from pymongo import MongoClient
from config import MONGODB_PORT, MONGODB_HOST, MONGODB_NAME
l111111lll_wcplus_ = MongoClient(MONGODB_HOST, MONGODB_PORT)
l11llllll_wcplus_ = l111111lll_wcplus_[MONGODB_NAME]

class l1l11llll_wcplus_:
    """
    mongodb
    """

    def __init__(self, table):
        """
        :param table: 实际上table在mongodb中被称为 collection 为了名称统一此处仍成为table
        table 的数据结果见data_scheme
        """
        self.table = l11llllll_wcplus_[table]

    def count(self, **kwargs):
        """
        :return:返回符合条件数据的总数
        """
        return self.table.find(kwargs).count()

    def delete(self, **kwargs):
        """
        :param kwargs: 用字典表示的过滤器
        :return: 根据match中提供的符合信息删除文章 支持全部删除
        """
        self.table.delete_many(kwargs)

    def get(self, **kwargs):
        """
        :param kwargs:
        :return: 返回符要求的数据生成器
        """
        data = self.table.find(kwargs)
        return data

    def insert(self, key, data, l111111ll1_wcplus_=True):
        """
        :param data: []多个数据，或单个数据{}
        :param key: 更新模式下判重的依据
        :param check_exist:是否需要检查存在(更新模式)
        :return: 插入一条数据或多个数据 在进行数据写入 基本上只需使用这一个API
        """
        res = 'INSERT'
        if l111111ll1_wcplus_:
            if type(data) == dict:
                res = self._111111l11_wcplus_(key, data)
            else:
                if type(data) == list:
                    res = self._11111l1l1_wcplus_(key, data)
                else:
                    if type(data) == dict:
                        self._insert_one(data)
                    else:
                        if type(data) == list:
                            self._11111l11l_wcplus_(data)
                return res

    def _insert_one(self, data):
        """
        :param data: {}
        :return: 插入一条数据
        """
        return self.table.insert_one(data).inserted_id

    def _11111l11l_wcplus_(self, data):
        """
        :param data: []
        :return: 插入多条数据
        """
        self.table.insert_many(data)
        return len(data)

    def _111111l11_wcplus_(self, key, data):
        """
        :param key: 判存字段
        :param data: {}
        :return: 更新或插入一条数据 用data中的字段更新key作为判断是否存在 存在更新 不存在就插入
        """
        result = self.table.find_one({key: data[key]})
        if type(result) is dict:
            self.table.update_one({key: data[key]}, {'$set': data})
            op_result = 'UPDATE'
        else:
            self._insert_one(data)
            op_result = 'INSERT'
        return op_result

    def _11111l1l1_wcplus_(self, key, data):
        """
        :param key: 判存字段
        :param data: []
        :return: 更新或插入多个数据 只要有一个数据是更新模式 返回UPDATE否则返回INSERT
        """
        res = 'INSERT'
        for d in data:
            if self._111111l11_wcplus_(key, d) == 'UPDATE':
                res = 'UPDATE'

        return res

    def l111111l1l_wcplus_(self):
        """
        :return: 返回table 方便用户自定义操作
        """
        return self.table


if __name__ == '__main__':
    data = {'video_num':0, 
     'pic_num':8,  'comment_id':'643962374688604160',  'id':'6b6934a83fa4385ed4ec53f987e07b5f'}
    col = l1l11llll_wcplus_('爱迪斯')
    col.insert('id', data)