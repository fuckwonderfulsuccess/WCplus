# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\l11ll1111_wcplus_.py


def l11ll11ll1_wcplus_(s, l1ll1l1111l_wcplus_='\n', l1ll1l11l1l_wcplus_=':'):
    """
    字符串到字典 支持自定义键值间隔符和成员间隔符
    :param s: 原字符串
    :param join_symbol: 连接符
    :param split_symbol: 分隔符
    :return: 字典
    """
    l1ll11lll1l_wcplus_ = s.split(l1ll1l1111l_wcplus_)
    data = dict()
    for item in l1ll11lll1l_wcplus_:
        item = item.strip()
        if item:
            k, v = item.split(l1ll1l11l1l_wcplus_, 1)
            data[k] = v.strip()

    return data


def l11l1ll1ll_wcplus_(data, l1ll1l1111l_wcplus_='&', l1ll1l11l1l_wcplus_='='):
    """
    :param data:dict数据
    :param join_symbol:不同成员之间的连接符
    :param split_symbol:名称和值分隔符
    :return: 字典转换为字符串
    """
    s = ''
    for k in data:
        s += str(k) + l1ll1l11l1l_wcplus_ + str(data[k]) + l1ll1l1111l_wcplus_

    return s[:-1]


def l11ll111l1_wcplus_(l1ll11lllll_wcplus_, l1ll1l11l11_wcplus_, keys=None):
    """
    :param whole_dict:
    :param part_dict:
    :param keys:
    :return:根据指定的keys 用part_dict的value更新whole_dict的value
    """
    if keys == None:
        l1ll11lllll_wcplus_.update(l1ll1l11l11_wcplus_)
        return l1ll11lllll_wcplus_
    for key in keys:
        if key in l1ll1l11l11_wcplus_:
            l1ll11lllll_wcplus_[key] = l1ll1l11l11_wcplus_[key]

    return l1ll11lllll_wcplus_


import hashlib

def l11llll11_wcplus_(data):
    """
    由于hash不处理unicode编码的字符串（python3默认字符串是unicode）
        所以这里判断是否字符串，如果是则进行转码
        初始化md5、将url进行加密、然后返回加密字串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    l1ll11llll1_wcplus_ = hashlib.md5()
    l1ll11llll1_wcplus_.update(data)
    return l1ll11llll1_wcplus_.hexdigest()