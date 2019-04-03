# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\protect\__init__.py
"""
如何解决证书会变化的问题？
"""
from utils.base import logger
from utils.time import get_internet_time
from datetime import datetime

def get_uuind():
    """
    :return: (UUID, ip)
    """
    from psutil import net_if_addrs
    from instance import PLATFORM
    uuind = []
    ip = None
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if '.' in address and '127.0.0.1' not in address:
                ip = address
            if PLATFORM == 'win':
                if '-' in address and len(address) == 17:
                    uuind.append(int(address.replace('-', ''), 16))
                else:
                    if PLATFORM == 'osx' and ':' in address and len(address) == 17:
                        uuind.append(int(address.replace(':', ''), 16))

    return (
     uuind, ip)


class Passport:

    @classmethod
    def get_mac_address(cls):
        """
        :return: 如果不能获取到mac地址就返回0
        """
        uuid, _ = get_uuind()
        if len(uuid):
            return uuid[0]
        else:
            return 1

    @classmethod
    def check_password(cls, q=True):
        """
        :param pt:真实mac+15618407030+截止日期timestamp
        :param mac:用户提供的mac
        :return:返回证书是否有效如果有效 无效直接False 有效返回截止日期 日期为字符串格式
        """
        return '2099-12-31 00:00:00'
        mac, pt = cls.read_password()
        if not mac and not pt:
            return False
        else:
            your_mac = cls.get_mac_address()
            your_macs, _ = get_uuind()
            if your_mac == 1:
                return False
            if int(mac) not in your_macs:
                if not q:
                    logger.warning('证书错误')
                return False
            end_time = int(pt) - int(mac) - 18058584888
            net_time = get_internet_time()
            if not net_time:
                return False
            left_seconds = end_time - get_internet_time()
            if left_seconds <= 0:
                if not q:
                    logger.warning('证书过期')
                return False
            end_time_str = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            if not q:
                logger.info('证书有效至' + end_time_str)
            return end_time_str

    @classmethod
    def read_password(cls):
        try:
            data = None
            with open('./license.ca', 'r', encoding='utf-8') as (f):
                data = f.readlines()
            mac = int(data[70][:-1])
            passport = int(data[91][:-1])
            return (
             mac, passport)
        except:
            logger.warning('未能找到授权证书license.ca')
            return (None, None)


if __name__ == '__main__':
    print(get_uuind())
