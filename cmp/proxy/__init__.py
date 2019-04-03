# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\proxy\__init__.py
"""
提供代理IP
"""
import requests, time
from instance import user_settings
from utils.base import logger
from utils.front import message_box

def get_proxy_ip(ips=1, source=0):
    """
    :param ips: 获取ip的数量
    :param source:0使用付费的芝麻IP 1使用开源的proxypool
    :return: 一个ip通过字符串形式返回 多个ip通过list形式返回
    """
    proxy = charge_proxy(ips)
    return proxy


def charge_proxy(ips):
    settings = user_settings.get()
    if 'proxy' in settings:
        ip_url = settings['proxy']
    else:
        logger.logger('请先设置代理IP')
        message_box('没有设置代理IP请先设置 设置之后请验证 确保返回的只有一个代理IP 例如 123.234.345.12:9808', '代理设置', 'error')
        return '127.0.0.1:1080'
        try:
            r_text = requests.get(ip_url).text
            if '白名单' in r_text:
                message_box('即将使用真实IP' + r_text, '获取代理IP出错', 'error')
                time.sleep(1)
                return '127.0.0.1:1080'
        except:
            message_box('请设置正确的代理IP 设置后请验证保证可返回一个代理IP 如果真实IP可用将使用真实IP进行采集', '代理设置', 'error')
            return '127.0.0.1:1080'
        else:
            while '请求' in r_text:
                time.sleep(1)
                r_text = requests.get(ip_url).text

            ip_ports = r_text.split('\r\n')[:-1]
            if len(ip_ports) == 1:
                return ip_ports[0]
            return ip_ports


def charge_proxy_2(ips):
    ip_url = 'http://webapi.http.zhimacangku.com/getip?num=*&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    ip_url = ip_url.replace('*', str(ips))
    r_text = requests.get(ip_url).text
    while '请求' in r_text:
        time.sleep(1)
        r_text = requests.get(ip_url).text

    ip_ports = r_text.split('\r\n')[:-1]
    if len(ip_ports) == 1:
        return ip_ports[0]
    else:
        return ip_ports


if __name__ == '__main__':
    print(get_proxy_ip(1))