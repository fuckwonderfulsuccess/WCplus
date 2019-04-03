# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\__init__.py


def db_select(des):
    """"
    :param des:
    :return: 根据数据保存目的返回正确的CollectionOperation
    """
    if des == 'FILE':
        from cmp.db.file import CollectionOperation
        return CollectionOperation
    if des == 'SQLITE':
        from cmp.db.sqlite import CollectionOperation
        return CollectionOperation
    return