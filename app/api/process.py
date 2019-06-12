# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\process.py
"""
采集进度管理
"""
from utils.base import l1lll1111_wcplus_

class Process:

    def __init__(self, l1l111ll1_wcplus_):
        """
        :param range: 采集范围 生成steps
        """
        self.l1l111ll1_wcplus_ = l1l111ll1_wcplus_
        self.process = {}
        steps = []
        s1 = {'title':'采集文章列表', 
         'des':'已经采集0篇文章', 
         'percent':0, 
         'color':'#ff000'}
        s2 = {'title':'采集正文', 
         'des':'文章数0/0 速度0', 
         'percent':0, 
         'color':'#ff00'}
        s3 = {'title':'采集阅读数据', 
         'des':'文章数0/0 速度0', 
         'percent':0, 
         'color':'#ff00ff'}
        if l1l111ll1_wcplus_ == 0:
            steps.append(s1)
        else:
            if l1l111ll1_wcplus_ == 25:
                steps.append(s1)
                steps.append(s2)
            else:
                if l1l111ll1_wcplus_ == 50:
                    steps.append(s1)
                    steps.append(s3)
                else:
                    if l1l111ll1_wcplus_ == 75:
                        steps.append(s1)
                        steps.append(s2)
                        steps.append(s3)
                    else:
                        if l1l111ll1_wcplus_ == 100:
                            steps.append(s3)
        self.process['steps'] = steps
        self.process['busy'] = 1
        self.process['current'] = 0

    def new_step(self):
        """
        :return: 发送新步骤开始
        """
        from utils.front import l1l11111l_wcplus_
        l1l11111l_wcplus_(title='采集进入新阶段', message=self.process['steps'][self.process['current']]['title'], _type='success', duration=5)
        self.process['current'] += 1
        self.l11l1ll11_wcplus_()

    def l11l1ll1l_wcplus_(self, l11ll11ll_wcplus_):
        """
        :param article_num:
        :return: 报告已经采集文章列表的总数
        """
        index = self.process['current'] - 1
        self.process['steps'][index]['des'] = ('已经采集*篇文章').replace('*', str(l11ll11ll_wcplus_))
        self.process['steps'][index]['percent'] = 0
        self.l11l1ll11_wcplus_()

    def l11l1l1ll_wcplus_(self, l11l1l1l1_wcplus_, l11ll1l11_wcplus_, proxy_ip, speed):
        """
        :param finished_num: 已经完成的文章数
        :param total_num: 总共需要采集的文章数
        :param proxy_ip: 当前代理ip
        :param speed: 速度
        :return: 采集完以一篇文章后发送进度
        """
        index = self.process['current'] - 1
        self.process['steps'][index]['des'] = '文章数%d/%d 速度%.3f篇/秒' % (l11l1l1l1_wcplus_, l11ll1l11_wcplus_, 1.0 / speed)
        self.process['steps'][index]['percent'] = round(l11l1l1l1_wcplus_ / l11ll1l11_wcplus_ * 100, 2)
        self.l11l1ll11_wcplus_()

    def l11l1lll1_wcplus_(self, l11l1l1l1_wcplus_, l11ll1l11_wcplus_, delay):
        """
        :param finished_num: 已经采集的文章数
        :param total_num: 文章总数
        :param delay: 采集间隔
        :return: 新采集到阅读数据之后发送进度
        """
        index = self.process['current'] - 1
        self.process['steps'][index]['des'] = '文章数%d/%d 速度%.3f篇/秒' % (l11l1l1l1_wcplus_, l11ll1l11_wcplus_, 1.0 / delay)
        self.process['steps'][index]['percent'] = round(l11l1l1l1_wcplus_ / l11ll1l11_wcplus_ * 100, 2)
        self.l11l1ll11_wcplus_()

    def l11l1ll11_wcplus_(self):
        """
        :return: 通过websocket发送数据
        """
        from l1l11_wcplus_ import socketio
        socketio.emit('process', self.process)

    def l1l11l1l1_wcplus_(self):
        self.process['busy'] = 0
        self.l11l1ll11_wcplus_()