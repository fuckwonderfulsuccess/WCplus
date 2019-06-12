# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\__init__.py


def l11l11ll1l_wcplus_(l11l11lll1_wcplus_):
    """"
    :param des:
    :return: 根据数据保存目的返回正确的CollectionOperation
    """
    if l11l11lll1_wcplus_ == 'FILE':
        from cmp.db.file import l1l11llll_wcplus_
        return l1l11llll_wcplus_
    if l11l11lll1_wcplus_ == 'SQLITE':
        from cmp.db.l11l11ll11_wcplus_ import l1l11llll_wcplus_
        return l1l11llll_wcplus_
    return