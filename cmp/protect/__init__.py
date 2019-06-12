# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\protect\__init__.py
from utils.base import logger
from utils.time import l1lll1l11ll_wcplus_
from datetime import datetime

def l1lll1l1lll_wcplus_():
    """
    :return: (UUID, ip)
    用该方法的返回的IP地址似乎有问题
    """
    from psutil import net_if_addrs
    from instance import l1_wcplus_
    l1lll1ll11l_wcplus_ = []
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if l1_wcplus_ == 'win':
                if '-' in address and len(address) == 17:
                    l1lll1ll11l_wcplus_.append(int(address.replace('-', ''), 16))
                else:
                    if l1_wcplus_ == 'osx' and ':' in address and len(address) == 17:
                        l1lll1ll11l_wcplus_.append(int(address.replace(':', ''), 16))

    return l1lll1ll11l_wcplus_


class Passport:

    @classmethod
    def l11l111l1_wcplus_(cls):
        uuid = l1lll1l1lll_wcplus_()
        if len(uuid):
            return uuid[0]
        else:
            return 1

    @classmethod
    def l1l11l111_wcplus_(cls, q=True):
        mac, pt = cls.l1lll1ll1l1_wcplus_()
        if not mac and not pt:
            return False
        else:
            l1lll1l1l11_wcplus_ = cls.l11l111l1_wcplus_()
            l1lll1l1ll1_wcplus_ = l1lll1l1lll_wcplus_()
            if l1lll1l1l11_wcplus_ == 1:
                return False
            if int(mac) not in l1lll1l1ll1_wcplus_:
                if not q:
                    logger.warning('证书错误')
                return False
            end_time = int(pt) - int(mac) - 12874767561234
            l1lll1ll111_wcplus_ = l1lll1l11ll_wcplus_()
            if not l1lll1ll111_wcplus_:
                return False
            l1lll1l11l1_wcplus_ = end_time - l1lll1l11ll_wcplus_()
            if l1lll1l11l1_wcplus_ <= 0:
                if not q:
                    logger.warning('证书过期')
                return False
            l1lll1l1l1l_wcplus_ = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            if not q:
                logger.info('证书有效至' + l1lll1l1l1l_wcplus_)
            return l1lll1l1l1l_wcplus_

    @classmethod
    def l1lll1ll1l1_wcplus_(cls):
        try:
            data = None
            with open('./license.ca', 'r', encoding='utf-8') as (f):
                data = f.readlines()
            mac = int(data[70][:-1])
            l11l11l1l_wcplus_ = int(data[91][:-1])
            return (
             mac, l11l11l1l_wcplus_)
        except:
            logger.warning('未能找到授权证书license.ca')
            return (None, None)


if __name__ == '__main__':
    print(l1lll1l1lll_wcplus_())