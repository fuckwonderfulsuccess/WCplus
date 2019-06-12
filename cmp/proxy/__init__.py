# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\proxy\__init__.py
"""
提供代理IP
"""
import requests, time
from instance import l1l1111ll_wcplus_
from utils.base import logger
from utils.front import l1l111lll_wcplus_

def l1ll1l1111_wcplus_(source=0):
    """
    :param source:0使用付费的芝麻IP 1使用开源的proxypool
    :return: 以字符串的形式返回一个IP 例如 171.13.149.40:26632
    """
    proxy = l1lll1l1111_wcplus_()
    return proxy


def l1lll1l1111_wcplus_():
    settings = l1l1111ll_wcplus_.get()
    print(settings)
    if 'proxy' in settings:
        l1lll1l111l_wcplus_ = settings['proxy']
    else:
        logger.logger('请先设置代理IP')
        l1l111lll_wcplus_('没有设置代理IP请先设置 设置之后请验证 确保返回的只有一个代理IP 例如 123.234.345.12:9808', '代理设置', 'error')
        return '127.0.0.1:1080'
        try:
            l1ll11ll11_wcplus_ = requests.get(l1lll1l111l_wcplus_).text
            if '白名单' in l1ll11ll11_wcplus_:
                l1l111lll_wcplus_('即将使用真实IP' + l1ll11ll11_wcplus_, '获取代理IP出错', 'error')
                time.sleep(1)
                return '127.0.0.1:1080'
        except:
            l1l111lll_wcplus_('请设置正确的代理IP 设置后请验证保证可返回一个代理IP 如果真实IP可用将使用真实IP进行采集', '代理设置', 'error')
            return '127.0.0.1:1080'
        else:
            while '请求' in l1ll11ll11_wcplus_:
                time.sleep(1)
                print('等待返回代理IP...')
                l1ll11ll11_wcplus_ = requests.get(l1lll1l111l_wcplus_).text

            return l1ll11ll11_wcplus_


if __name__ == '__main__':
    print(l1ll1l1111_wcplus_(1))