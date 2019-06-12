# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\l11l11ll11_wcplus_\__init__.py
from cmp.db.l11l11ll11_wcplus_.l1111l1ll1_wcplus_ import l1lllllll11_wcplus_
from utils.base import logger

class l1l11llll_wcplus_:
    """
    提供sqllite的API
    使用时传入一个data_schema中的类即可
    正确的做法应该是使用sql语句操作 以后再来更新 接口
    详细文档见 http://docs.peewee-orm.com/en/latest/peewee/query_operators.html
    """

    def __init__(self, table):
        self.table = table

    def count(self, key=None, value=None, _type=1):
        """
        :param key: 来自Data中的某个属性
        :param value: 希望匹配概述性的值
        :param _type: 1:包含模式 2:相等模式
        :return:返回符合条件数据的总数
        """
        if _type == 1:
            return self.table.select().where(getattr(self.table, key).contains(value)).count()
        if _type == 2:
            return self.table.select().where(getattr(self.table, key) == value).count()

    def delete(self, key=None, value=None, _type=1):
        """
        :param key:
        :param value:
        :return: 删除符合条件的数据
        """
        if key:
            if _type == 1:
                query = self.table.delete().where(getattr(self.table, key).contains(value))
            else:
                if _type == 2:
                    query = self.table.delete().where(getattr(self.table, key) == value)
                else:
                    query = self.table.delete()
                return query.execute()

    def get(self, key=None, value=None, _type=1):
        """
        :param key:
        :param value:
        :param _type: 1:包含模式 2:相等模式
        :return: 返回符合查询结果的数据
        """
        if key:
            if _type == 1:
                return self.table.select().where(getattr(self.table, key).contains(value))
            if _type == 2:
                return self.table.select().where(getattr(self.table, key) == value)
        else:
            return self.table.select()

    def insert(self, data):
        """
        :param data:list或dict
        :return: 不存在插入 存在更新 同时支持单个数据和多个数据
        单个数据使用dict表示 多个数据使用list表示
        """
        res = None
        if type(data) is type({}):
            exist = self.count('id', data['id'], _type=2)
            if exist == 0:
                self.table.create(**data)
                res = 'INSERT'
            else:
                self.update('id', data['id'], data)
                res = 'UPDATE'
            return res
        if type(data) is type([]):
            with l1lllllll11_wcplus_.atomic():
                for d in data:
                    exist = self.count('id', d['id'], _type=2)
                    if exist == 0:
                        self.table.create(**d)
                        res = 'INSERT'
                    else:
                        self.update('id', d['id'], d)
                        res = 'UPDATE'

            return res
        logger.error('待插入的数据有误%s' % str(data))
        return 'ERROR'

    def update(self, key, value, data):
        """
        :param key:
        :param value:
        :param data:
        :return: 更新一条数据
        """
        query = (self.table.update(**data)).where(getattr(self.table, key) == value)
        return query.execute()

    def l111111l1l_wcplus_(self):
        """
        :return: 返回table 方便用户自定义操作
        """
        return self.table


if __name__ == '__main__':
    pass