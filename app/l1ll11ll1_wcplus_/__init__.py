# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\__init__.py
"""
管理所有的爬虫
1. 利用rq对象统从数据源或请求参数 为了减少数据库操作的频率 缓存该数据
"""
import time

class l1ll1ll1ll_wcplus_:
    """
    管理爬虫的暂停或启动 每种爬虫的最频繁动作都会调用它的某个方法
    该方法要么一直卡壳直到满足某种状态 要么直接放行
    他是一个岗哨或者是一个检查站 会被设置在流量入口 通过token验证对方的状态
    岗哨还要能接受外部的指令 可改变通行规则
    更多的规则陆续加入
    """

    def __init__(self):
        self.pause = False

    def stop(self):
        self.pause = True

    def start(self):
        self.pause = False

    def check(self, token):
        """
        :param token: {'crawler':'爬虫名称', 'msg':'judge返回的结果'}
        :return: 安置在流量入口 通过对方的token和本身的规则决定是否放行
        如果不能放行 根据对方不能通过的原因 主动处理异常（重新获取参数）或者等待更新放行规则（比如从暂停中恢复采集）
        """
        while self.pause:
            time.sleep(0.1)

        if token['msg'] == 'req_data_error':
            self.pause = True
            from utils.front import l1l111lll_wcplus_
            l1l111lll_wcplus_('需要重新操作当前公众号 获取参数' + token['crawler'], '参数错误', 'error')
            while self.pause:
                time.sleep(0.1)