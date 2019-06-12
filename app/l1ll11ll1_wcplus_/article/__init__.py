# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\article\__init__.py
"""
得到的请求参数全部的微信账号进行采集
多线程爬取微信公众号文章正文
使用前提条件：
1. 数据库有文章的永久链接
2. 代理IP地址有效
"""
import threading, os, codecs
from lxml.etree import tostring
from queue import Queue
import requests
from requests.exceptions import SSLError, Timeout, ProxyError, ConnectionError
import queue, time
from cmp.proxy import l1ll1l1111_wcplus_
from copy import copy
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
from utils.base import logger
from utils.l11ll1111_wcplus_ import l11llll11_wcplus_
from instance import l1l1111ll_wcplus_
if 'save_html' in l1l1111ll_wcplus_.get():
    l1ll11l1ll_wcplus_ = l1l1111ll_wcplus_.get()['save_html']
else:
    l1ll11l1ll_wcplus_ = 'false'
l1l1l1111l_wcplus_ = []
nickname = None
l1ll1l11ll_wcplus_ = None
l11ll111l_wcplus_ = None

class l1ll111lll_wcplus_(threading.Thread):
    """
    继承threading.Thread 定义任务处理类
    1. 从任务队列中取出一个任务
    2. 从代理IP队列中取出一个IP 发起请求 如果请求成功将代理IP放回队列 否者重新申请一个代理IP再次发起请求直到成功
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    def __init__(self, l1l11l111l_wcplus_, l1l111l1l1_wcplus_):
        """
        :param task_q: 任务队列
        :param ip_q: 代理IP队列
        """
        threading.Thread.__init__(self)
        self.l1l11l111l_wcplus_ = l1l11l111l_wcplus_
        self.l1l111l1l1_wcplus_ = l1l111l1l1_wcplus_
        self.l1l111lll1_wcplus_ = False

    def run(self):
        """
        :return: 直到线程结束
        """
        while not self.l1l111lll1_wcplus_:
            result = self.l1l1ll1111_wcplus_()
            if result is None:
                self.l1l111lll1_wcplus_ = True
                break

    def stop(self):
        self.l1l111lll1_wcplus_ = True

    @property
    def l1l1l1l1ll_wcplus_(self):
        """
        :return: 尝试从任务队列中取出一个任务
        """
        try:
            task = self.l1l11l111l_wcplus_.get(block=True, timeout=20)
            return task
        except queue.Empty:
            return

    def l1l11l1111_wcplus_(self):
        """
        :return: 申请一个代理IP
        """
        proxy_ip = l1ll1l1111_wcplus_()
        if not proxy_ip:
            self.l1l11l111l_wcplus_.clear()
            logger.error('采集文章正文:' + 'IP地址被限制！采集文章正文已经提前结束，将导致部分文章的PDF无法导出，可24小时后再次采集，亦可联系阿呆。将继续采集阅读数据')
        l1l1ll1l11_wcplus_.l1l111l11l_wcplus_(ip=proxy_ip, l1l11lllll_wcplus_=time.time())
        return proxy_ip

    def l1ll111l11_wcplus_(self, all=False):
        """
        :param all: True全部取出 False取出下一个可用的代理
        :return: 取出代理IP
        """
        if self.l1l111l1l1_wcplus_.qsize():
            ips = self.l1l111l1l1_wcplus_.get(block=True, timeout=None)
            self.l1l111l1l1_wcplus_.put(ips, block=True, timeout=None)
            if all:
                return ips['ips']
            return (
             ips['ips'][ips['next_ip']], ips['next_ip'])
        else:
            exit('代理IP队列出现错误')

    def l1l1l11111_wcplus_(self, proxy_ip, index):
        """
        :param proxy_ip:
        :return: 更新队列中的proxy_ip 返回队列中代理IP的数量
        """
        ips = self.l1l111l1l1_wcplus_.get(block=True, timeout=None)
        ips['ips'][index] = proxy_ip
        self.l1l111l1l1_wcplus_.put(ips, block=True, timeout=None)
        return len(ips['ips'])

    def l1l11lll1l_wcplus_(self):
        """
        :return:next_ip有效自增
        """
        ips = self.l1l111l1l1_wcplus_.get(block=True, timeout=None)
        ips['next_ip'] = (ips['next_ip'] + 1) % len(ips['ips'])
        self.l1l111l1l1_wcplus_.put(ips, block=True, timeout=None)
        return ips['next_ip']

    def l1l1ll1111_wcplus_(self):
        """
        :return: 取出一个任务 请求html内容
        """
        global l11ll111l_wcplus_
        global nickname
        task = self.l1l1l1l1ll_wcplus_
        if task is None:
            return
        else:
            proxy_ip, index = self.l1ll111l11_wcplus_()
            l1l11l11l1_wcplus_ = False
            l1ll11ll11_wcplus_ = None
            l1l1lll1l1_wcplus_ = False
            l1lll11l1l_wcplus_ = copy(task['content_url'])
            while not l1l11l11l1_wcplus_:
                try:
                    if '127.0.0.1' in proxy_ip['ip']:
                        if 'https' not in task['content_url']:
                            task['content_url'] = task['content_url'].replace('http', 'https')
                        r = requests.get(url=task['content_url'], headers=self.headers,
                          timeout=5)
                    else:
                        r = requests.get(url=task['content_url'], headers=self.headers,
                          timeout=5,
                          proxies={'http':proxy_ip['ip'], 
                         'https':proxy_ip['ip']})
                    l1ll11ll11_wcplus_ = r.text
                    if '访问过于频繁，请用微信扫描二维码进行访问' in l1ll11ll11_wcplus_ or '<title>验证</title>' in l1ll11ll11_wcplus_ or 'IP Address:' in l1ll11ll11_wcplus_:
                        logger.error('IP被限制:' + task['content_url'])
                        l1l1ll1l11_wcplus_.l1ll11111l_wcplus_(proxy_ip['ip'], 'IP被限制')
                        if l1l1ll1l11_wcplus_.l1ll111ll1_wcplus_(proxy_ip['ip']):
                            proxy_ip['ip'] = self.l1l11l1111_wcplus_()
                        l1l1lll1l1_wcplus_ = True
                    else:
                        l1l1llll1l_wcplus_ = l1llllll11_wcplus_.decode_content(l1ll11ll11_wcplus_, l1l11l1l11_wcplus_=True)
                        l1l1llll1l_wcplus_['id'] = l11llll11_wcplus_(task['content_url'].replace('https', 'http'))
                        if l1ll11l1ll_wcplus_ == 'true':
                            l1llllll11_wcplus_.l1l11ll111_wcplus_(nickname=nickname, file_name=l1l1llll1l_wcplus_['id'], l1l1l11l11_wcplus_=l1ll11ll11_wcplus_)
                        l11ll111l_wcplus_.insert('id', l1l1llll1l_wcplus_)
                        l1l11l11l1_wcplus_ = True
                except ProxyError:
                    l1l1lll1l1_wcplus_ = True
                    print(task['id'], proxy_ip, 'ProxyError', task['content_url'])
                    l1l1ll1l11_wcplus_.l1ll11111l_wcplus_(proxy_ip['ip'], 'ProxyError')
                    if l1l1ll1l11_wcplus_.l1ll111ll1_wcplus_(proxy_ip['ip']):
                        proxy_ip['ip'] = self.l1l11l1111_wcplus_()
                except SSLError:
                    l1l1lll1l1_wcplus_ = True
                    print(task['id'], proxy_ip, 'SSLError')
                    l1l1ll1l11_wcplus_.l1ll11111l_wcplus_(proxy_ip['ip'], 'SSLError')
                    if l1l1ll1l11_wcplus_.l1ll111ll1_wcplus_(proxy_ip['ip']):
                        proxy_ip['ip'] = self.l1l11l1111_wcplus_()
                except Timeout:
                    l1l1lll1l1_wcplus_ = True
                    print(task['id'], proxy_ip, 'Timeout')
                    l1l1ll1l11_wcplus_.l1ll11111l_wcplus_(proxy_ip['ip'], 'Timeout')
                    if l1l1ll1l11_wcplus_.l1ll111ll1_wcplus_(proxy_ip['ip']):
                        proxy_ip['ip'] = self.l1l11l1111_wcplus_()
                except ConnectionError:
                    l1l1lll1l1_wcplus_ = True
                    print(task['id'], proxy_ip, 'ConnectionError')
                    l1l1ll1l11_wcplus_.l1ll11111l_wcplus_(proxy_ip['ip'], 'ConnectionError')
                    if l1l1ll1l11_wcplus_.l1ll111ll1_wcplus_(proxy_ip['ip']):
                        proxy_ip['ip'] = self.l1l11l1111_wcplus_()
                except Exception as e:
                    template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                    message = template.format(type(e).__name__, e.args)
                    print(message)

            self.l1l11l111l_wcplus_.task_done()
            if l1l1lll1l1_wcplus_:
                self.l1l1l11111_wcplus_(proxy_ip, index)
            self.l1l11lll1l_wcplus_()
            l1l1ll1l11_wcplus_.l1ll1l1l1l_wcplus_(proxy_ip['ip'])
            l1l1ll1l11_wcplus_.l1l1l11lll_wcplus_()
            return l1ll11ll11_wcplus_

    def l1l1lll111_wcplus_(self, r):
        """
        :param r:
        :return: 判断请求相应是否是有效的文章html
        """
        pass


class l1l11llll1_wcplus_:
    """
    服务于Worker，代理IP的数量和线程的数量可以不一致
    """

    def __init__(self, nickname, l1l11l111l_wcplus_, l1l111l1l1_wcplus_):
        """
        :param nickname: 需要爬取公众号文章的昵称
        :param task_q: 全局可见任务队列
        :param ip_q: 全局可见代理IP队列
        """
        self.l1l11l111l_wcplus_ = l1l11l111l_wcplus_
        self.l1l111l1l1_wcplus_ = l1l111l1l1_wcplus_
        self.nickname = nickname
        self.l1l1ll111l_wcplus_ = l11ll111l_wcplus_.get(article={'$exists': False})
        self.l1l1lll11l_wcplus_ = l11ll111l_wcplus_.count(article={'$exists': False})
        self.l1l1l1lll1_wcplus_ = 0
        logger.debug('%s共有%d篇文章' % (self.nickname, self.l1l1lll11l_wcplus_))
        self.begin_time = time.time()
        self.l1l1l111l1_wcplus_ = None
        self.l1ll11lll_wcplus_ = None

    def l1l1ll1l1l_wcplus_(self):
        """
        :return: 创建任务队列 将待爬取的文章加入任务队列
        """
        index = 0
        for a in self.l1l1ll111l_wcplus_:
            if 'mp.weixin.qq.com' in a['content_url']:
                index += 1
                task = {'nickname':a['nickname'],  'title':a['title'],  'content_url':a['content_url'],  'id':index}
                self.l1l11l111l_wcplus_.put(task, block=True, timeout=None)

        self.l1l1l1lll1_wcplus_ = index
        logger.debug('%s共有%d篇文章需要爬取' % (self.nickname, self.l1l1l1lll1_wcplus_))
        l1l1ll1l11_wcplus_.l1l1111lll_wcplus_(self.l1l1l1lll1_wcplus_)
        return self.l1l1l1lll1_wcplus_

    def l1ll1l1l11_wcplus_(self, l1l1111ll1_wcplus_=1, proxy=False):
        """
        :param ip_num: 代理的数量
        :param proxy: 是否需要使用代理否者代理IP全部为 127.0.0.1:80 如果proxy为False代理ip默认为一个127.0.0.1:80
        :return: 初始化代理IP队列
        队列只有一个任务 数据类型为dict
        {'ips':[{'ip':ip,'delay':0,'alive_time':0,'cunter':0},{***},{***}],
         'next_ip':0}
        ips是全部可用ip的list
        next_ip有上一次使用的进程更新 下一个进程使用其确定使用哪个ip
        """
        ips = []
        self.l1l1l111l1_wcplus_ = True
        if proxy == False:
            ips = '127.0.0.1:80'
        else:
            if l1l1111ll1_wcplus_ == 1:
                ips = l1ll1l1111_wcplus_()
            else:
                ips = [l1ll1l1111_wcplus_() for i in range(l1l1111ll1_wcplus_)]
                self.l1l1l111l1_wcplus_ = False
        if type(ips) == str:
            ips = [
             ips]
        l1l1lllll1_wcplus_ = {}
        l1l1lllll1_wcplus_['ips'] = []
        l1l1lllll1_wcplus_['next_ip'] = 0
        for ip in ips:
            logger.debug(ip)
            l1l1lllll1_wcplus_['ips'].append({'ip':ip,  'delay':0,  'alive_time':0,  'cunter':0})
            l1l1ll1l11_wcplus_.l1l111l11l_wcplus_(ip=ip, l1l11lllll_wcplus_=time.time())

        self.l1l111l1l1_wcplus_.put(l1l1lllll1_wcplus_, block=True, timeout=None)
        logger.debug(l1l1lllll1_wcplus_)
        logger.debug('代理IP队列已经初始化完毕 共有%d个代理代理IP' % self.l1l111l1l1_wcplus_.qsize())


class l1l1ll1l11_wcplus_:
    """
    记录任务执行过程中的信息
    """
    l1l111l1ll_wcplus_ = {'ips_index':[],  'ips':{},  'total_task_num':0, 
     'done_task_num':0, 
     'ip_used':0, 
     'begin_time':0, 
     'speed':0, 
     'worker_num':0}
    l1l11l11ll_wcplus_ = {'ip':'', 
     'created_time':0, 
     'last_time':0, 
     'used_unm':0, 
     'speed':0, 
     'failed':0, 
     'reason':[]}
    l1ll11llll_wcplus_ = None

    @staticmethod
    def l1l11ll1l1_wcplus_(l1ll11llll_wcplus_):
        l1l1ll1l11_wcplus_.l1ll11llll_wcplus_ = l1ll11llll_wcplus_
        ts = copy(l1l1ll1l11_wcplus_.l1l111l1ll_wcplus_)
        ts['begin_time'] = time.time()
        l1l1ll1l11_wcplus_.l1ll11llll_wcplus_.put(ts, block=True, timeout=None)

    @staticmethod
    def l1l1111lll_wcplus_(l1l11ll1ll_wcplus_):
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        ts['total_task_num'] = l1l11ll1ll_wcplus_
        result = l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        if result == None:
            logger.error('任务状态队列出错')
            exit()

    @staticmethod
    def l1l111l111_wcplus_(l1ll11lll_wcplus_):
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        ts['worker_num'] = l1ll11lll_wcplus_
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)

    @staticmethod
    def l1l111l11l_wcplus_(**kwargs):
        """
        :param kwargs:
        :return: 根据'ip'更新代理ip的日志 ip参数必须指定
        """
        ip = kwargs['ip']
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        if ip in ts['ips_index']:
            ts['ips'][ip].update(kwargs)
        else:
            ts['ips_index'].append(ip)
            l1l11l11ll_wcplus_ = copy(l1l1ll1l11_wcplus_.l1l11l11ll_wcplus_)
            l1l11l11ll_wcplus_.update(kwargs)
            ts['ips'][ip] = l1l11l11ll_wcplus_
            ts['ip_used'] += 1
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)

    @staticmethod
    def l1l111ll1l_wcplus_(ip):
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        ts['ips'][ip]['used_unm'] += 1
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)

    @staticmethod
    def l1ll1l1l1l_wcplus_(ip):
        """
        :param ip:
        :return: 当代理ip完成一次爬取之后调用该方法自动计算机相关数据
        """
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        ts['ips'][ip]['used_unm'] += 1
        ts['ips'][ip]['last_time'] = time.time()
        ts['ips'][ip]['speed'] = round((ts['ips'][ip]['last_time'] - ts['ips'][ip]['created_time']) / ts['ips'][ip]['used_unm'], 3)
        ts['done_task_num'] += 1
        ts['speed'] = round((time.time() - ts['begin_time']) / ts['done_task_num'], 3)
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)

    @staticmethod
    def l1ll11111l_wcplus_(ip, l1ll1111ll_wcplus_):
        """
        :param ip:
        :param failed_reason:
        :return: 添加ip失败标记
        """
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        ts['ips'][ip]['failed'] += 1
        ts['ips'][ip]['reason'].append(l1ll1111ll_wcplus_)
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)

    @staticmethod
    def l1l1111l11_wcplus_(ip):
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        return ts['ips'][ip]['failed']

    @staticmethod
    def l1ll111ll1_wcplus_(ip):
        """
        :return: 对于一个刚才发生失败请求的IP是否应该申请新IP
        如果一IP失败的次数小于 线程数 则不应该申请新IP
        """
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        l1l1lll1ll_wcplus_ = ts['ips'][ip]['failed']
        l1ll11lll_wcplus_ = ts['worker_num']
        logger.warning('ip:%s 失败次数:%d 任务总数:%d' % (ip, l1l1lll1ll_wcplus_, l1ll11lll_wcplus_))
        if l1l1lll1ll_wcplus_ < l1ll11lll_wcplus_:
            return False
        else:
            ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
            ts['ips'][ip]['failed'] = 0
            l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
            return True

    @staticmethod
    def l1ll11ll1l_wcplus_():
        """
        :return: 从队列中获取任务状态
        """
        if l1l1ll1l11_wcplus_.l1ll11llll_wcplus_.qsize() == 0:
            return
        else:
            ts = l1l1ll1l11_wcplus_.l1ll11llll_wcplus_.get(block=True, timeout=None)
            return ts

    @staticmethod
    def l1l11l1ll1_wcplus_(ts):
        """
        :param ts: 将任务状态存瑞任务队列中
        :return:
        """
        if l1l1ll1l11_wcplus_.l1ll11llll_wcplus_.qsize() == 1:
            return
        else:
            l1l1ll1l11_wcplus_.l1ll11llll_wcplus_.put(ts, block=True, timeout=None)
            return ts

    @staticmethod
    def l1l11ll11l_wcplus_():
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        logger.info(ts)

    @staticmethod
    def l1l1l11lll_wcplus_():
        global l1ll1l11ll_wcplus_
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        item = {}
        item['style'] = '采集正文'
        item['nickname'] = '略'
        item['process'] = '%d/%d' % (ts['done_task_num'], ts['total_task_num'])
        item['data'] = '速度%.3f' % ts['speed']
        item['task'] = '略'
        logger.info('速度%.3f 完成%d/%d' % (ts['speed'], ts['done_task_num'], ts['total_task_num']))
        if l1ll1l11ll_wcplus_:
            l1ll1l11ll_wcplus_.l11l1l1ll_wcplus_(ts['done_task_num'], ts['total_task_num'], ts['ips'], ts['speed'])

    @staticmethod
    @property
    def l1l1l111ll_wcplus_():
        ts = l1l1ll1l11_wcplus_.l1ll11ll1l_wcplus_()
        l1l1ll1l11_wcplus_.l1l11l1ll1_wcplus_(ts)
        return ts['ip_used']


class l1ll11lll1_wcplus_:
    """
    多线程爬取微信公众号的文章正文
    """

    def __init__(self):
        self.l1l11l111l_wcplus_ = Queue()
        self.l1l111l1l1_wcplus_ = Queue()
        l1l1ll1l11_wcplus_.l1l11ll1l1_wcplus_(Queue())
        self.ws = None
        self.l1l1l1llll_wcplus_ = []

    def l1l1l1l11l_wcplus_(self, nickname, l1ll11lll_wcplus_=16, l1l1111ll1_wcplus_=1, l1l1llll11_wcplus_=False):
        """
        :param nickname: 公众号昵称用于从数据库中获取需要爬取内容的文章
        :param worker_num: 通过发起请求的线程数量
        :param ip_num: 使用的代理IP数量
        :param need_proxy: 是否需要设置代理，设置为不需要，如果被限制会自动使用代理
        :param one_proxy: 是否使用同一个代理IP进行多线程请求
        :return:
        """
        self.ws = l1l11llll1_wcplus_(nickname, self.l1l11l111l_wcplus_, self.l1l111l1l1_wcplus_)
        l1l1l1lll1_wcplus_ = self.ws.l1l1ll1l1l_wcplus_()
        self.ws.l1ll1l1l11_wcplus_(l1l1111ll1_wcplus_=l1l1111ll1_wcplus_, proxy=l1l1llll11_wcplus_)
        l1l1ll1l11_wcplus_.l1l111l111_wcplus_(l1ll11lll_wcplus_)
        l1l1ll1l11_wcplus_.l1l11ll11l_wcplus_()
        self.l1l1l1llll_wcplus_ = []
        for i in range(l1ll11lll_wcplus_):
            self.l1l1l1llll_wcplus_.append(l1ll111lll_wcplus_(self.l1l11l111l_wcplus_, self.l1l111l1l1_wcplus_))

        return l1l1l1lll1_wcplus_

    def l1ll1l11l1_wcplus_(self):
        for l1ll11l111_wcplus_ in self.l1l1l1llll_wcplus_:
            l1ll11l111_wcplus_.start()

    def l1l111ll11_wcplus_(self):
        for l1ll11l111_wcplus_ in self.l1l1l1llll_wcplus_:
            l1ll11l111_wcplus_.join()


l1l1ll11ll_wcplus_ = 'nickname">\\n\\S*?</strong>'
l1l1l11l1l_wcplus_ = 'video_iframe'
l1l111llll_wcplus_ = '<img '
l1l1111l1l_wcplus_ = 'comment_id = "\\S*?"'
import re, html2text
l1111l1l1_wcplus_ = html2text.HTML2Text()

class l1llllll11_wcplus_:
    """
    解析文章内容
    """

    @staticmethod
    def decode_content(r, l1l11l1l11_wcplus_=True):
        """
        :param r:html字符串
        :return:解析文章html
        文章html中包含的信息非常丰富 不仅仅只有文章文本等基本数据还有comment_id
        video_num pic_num 还有原文的markdown信息
        """
        data = {}
        l1ll1l111l_wcplus_ = r
        data['video_num'] = len(re.findall(l1l1l11l1l_wcplus_, l1ll1l111l_wcplus_))
        data['pic_num'] = len(re.findall(l1l111llll_wcplus_, l1ll1l111l_wcplus_))
        data['comment_id'] = re.findall(l1l1111l1l_wcplus_, l1ll1l111l_wcplus_)
        if len(data['comment_id']) == 1:
            data['comment_id'] = data['comment_id'][0].split('"')[1]
        else:
            data['comment_id'] = str(0)
        if l1l11l1l11_wcplus_:
            try:
                l1ll1l111l_wcplus_ = l1llllll11_wcplus_.l111l1111_wcplus_(l1ll1l111l_wcplus_)
                data['article'] = l1111l1l1_wcplus_.handle(l1ll1l111l_wcplus_).replace('\n', '')
            except Exception as e:
                try:
                    data['article'] = l1111l1l1_wcplus_.handle(r).replace('\n', '')
                except:
                    data['article'] = ''

            return data

    @staticmethod
    def l1l11ll111_wcplus_(nickname, file_name, l1l1l11l11_wcplus_):
        """
        :param nickname: 公众号的昵称用作文件夹
        :param html_str: html内容
        :param file_name: 文件名
        :return: 将文章的html内容保存为文件 存储在web_server的static/html/nickname路径下
        """
        path = './web_server/static/html/' + nickname + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        l1ll1l1ll1_wcplus_ = path + file_name + '.html'
        if not os.path.isfile(l1ll1l1ll1_wcplus_):
            file = codecs.open(l1ll1l1ll1_wcplus_, 'w', 'utf-8')
            file.write(l1l1l11l11_wcplus_.replace('data-src', 'src'))
            file.close()
        else:
            logger.debug('HTML已存在 %s' % l1ll1l1ll1_wcplus_)

    @staticmethod
    def l111l1111_wcplus_(l1l1ll11l1_wcplus_, l1ll11l1l1_wcplus_='//div[@id="js_content"]'):
        """
        :param x_path:xpath表达式默认获取微信公众号的正文xpath
        :param raw_html:r.text
        :return: 截取html的一部分
        """
        from lxml import html
        tree = html.fromstring(l1l1ll11l1_wcplus_)
        data = tree.xpath(l1ll11l1l1_wcplus_)
        if len(data) == 1:
            data = tostring(data[0], encoding='unicode')
            return data
        return l1l1ll11l1_wcplus_


def l1l1ll1lll_wcplus_(l1l1l1l1l1_wcplus_=200):
    """
    :return: article_data_buffer当到达一定长度之后 保存并清空
    """
    global l1l1l1111l_wcplus_
    success = False
    if len(l1l1l1111l_wcplus_) >= l1l1l1l1l1_wcplus_:
        while not success:
            try:
                l11ll111l_wcplus_.insert(id, l1l1l1111l_wcplus_)
                l1l1l1111l_wcplus_ = []
                logger.info('保存成功保存%d' % l1l1l1l1l1_wcplus_)
                success = True
            except:
                time.sleep(3)
                l1l1ll1lll_wcplus_(l1l1l1l1l1_wcplus_=l1l1l1l1l1_wcplus_)


def l1l11lll11_wcplus_():
    """
    :return: 是否直接使用代理
    """
    from instance import l1l1111ll_wcplus_
    settings = l1l1111ll_wcplus_.get()
    if 'use_proxy' in settings:
        if settings['use_proxy'] == 'true':
            return False
        return True
    else:
        return False


def l1l1ll1ll_wcplus_(l1ll11lll_wcplus_=128, process=None):
    global l11ll111l_wcplus_
    global l1l1l1111l_wcplus_
    global l1ll1l11ll_wcplus_
    global nickname
    l1ll1l11ll_wcplus_ = process
    l1l1l1111l_wcplus_ = []
    from instance import rd
    nickname = rd.l1ll11l1l_wcplus_()[0]['nickname']
    l11ll111l_wcplus_ = l1l11llll_wcplus_(nickname)
    rc = l1ll11lll1_wcplus_()
    l1l1l1lll1_wcplus_ = rc.l1l1l1l11l_wcplus_(nickname, l1ll11lll_wcplus_=l1ll11lll_wcplus_, l1l1111ll1_wcplus_=1, l1l1llll11_wcplus_=l1l11lll11_wcplus_())
    if not l1l1l1lll1_wcplus_:
        return
    rc.l1ll1l11l1_wcplus_()
    rc.l1l111ll11_wcplus_()
    l1l1ll1l11_wcplus_.l1l11ll11l_wcplus_()


def l1ll1111l_wcplus_(_1l1l1ll1l_wcplus_, l1ll11lll_wcplus_=128, process=None):
    global l11ll111l_wcplus_
    global l1l1l1111l_wcplus_
    global l1ll1l11ll_wcplus_
    global nickname
    l1ll1l11ll_wcplus_ = process
    l1l1l1111l_wcplus_ = []
    nickname = _1l1l1ll1l_wcplus_
    l11ll111l_wcplus_ = l1l11llll_wcplus_(nickname)
    rc = l1ll11lll1_wcplus_()
    l1l1l1lll1_wcplus_ = rc.l1l1l1l11l_wcplus_(nickname, l1ll11lll_wcplus_=l1ll11lll_wcplus_, l1l1111ll1_wcplus_=1, l1l1llll11_wcplus_=l1l11lll11_wcplus_())
    if not l1l1l1lll1_wcplus_:
        return
    rc.l1ll1l11l1_wcplus_()
    rc.l1l111ll11_wcplus_()
    l1l1ll1l11_wcplus_.l1l11ll11l_wcplus_()


if __name__ == '__main__':
    l1ll1111l_wcplus_('人民日报')