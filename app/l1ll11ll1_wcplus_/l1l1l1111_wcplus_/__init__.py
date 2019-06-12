# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\l1l1l1111_wcplus_\__init__.py
"""
管理请求参数 接受爬虫参数是否过期的指令 提供自动或手动更新参数的方法
全局只有一个实例 参数既可以被动更新 在自动模式之下也可以定时更新
定时更新的好处在于 后台自动更新不用等待 整个采集过程完整
1. 从指定地方库读取参数
2. 整理请求参数
3. 报告请求参数的状态
4. 调用自动获取参数的接口
"""
import json
from datetime import datetime
from instance import l11l1l1ll1_wcplus_

class l1111_wcplus_:

    def __init__(self):
        self.l1l11ll11_wcplus_ = []
        self.l1l11ll1l_wcplus_ = []

    def clean(self):
        """
        进行数据的初步处理
        1. 从数据源获取原始数据
        2. 基本格式转化
        3. 添加部分字段
        """
        self.l1l11ll11_wcplus_ = []
        l11l1l11l1_wcplus_ = l11l1l1ll1_wcplus_.get()
        for rd in l11l1l11l1_wcplus_:
            item = {}
            item['key'] = rd['key']
            item['time'] = datetime.timestamp(rd['time'])
            if rd['value'][0] == '{':
                item['value'] = json.loads(rd['value'])
            else:
                item['value'] = rd['value']
            self.l1l11ll11_wcplus_.append(item)

    def l1ll11l1l_wcplus_(self):
        """
        :return: 分组 返回一个list 格式如下
        [
            {'nick_name': '微信昵称',
             'nickname': '公众号名称',
             'home': '点击全部消息的主页',
             'load_more': '加载更多历史消息',
             'content': '文章正文',
             'appmsg_comment': '评论',
             'getappmsgext': '阅读数据',},
        ]
        """
        self.clean()
        nickname = 'UNK'
        l1l11ll1l_wcplus_ = []
        l11l1l11ll_wcplus_ = {}
        for rd in self.l1l11ll11_wcplus_:
            item = {}
            if rd['key'] == 'current_nickname':
                nickname = rd['value']
            elif 'req' in rd['key']:
                keys = rd['key'].split('.')
                if keys[0] not in l11l1l11ll_wcplus_:
                    l11l1l11ll_wcplus_[keys[0]] = {}
                l11l1l11ll_wcplus_[keys[0]][keys[1]] = rd['value']
                l11l1l11ll_wcplus_[keys[0]][keys[1]]['time'] = rd['time']
            elif 'nick_name' in rd['key']:
                keys = rd['key'].split('.')
                if rd['value'] not in l11l1l11ll_wcplus_:
                    l11l1l11ll_wcplus_[rd['value']] = {}
                l11l1l11ll_wcplus_[rd['value']]['nick_name'] = keys[0]

        for key in l11l1l11ll_wcplus_:
            item = l11l1l11ll_wcplus_[key]
            item['wxuin'] = key
            item['nickname'] = nickname
            l1l11ll1l_wcplus_.append(item)

        self.l1l11ll1l_wcplus_ = l1l11ll1l_wcplus_
        return l1l11ll1l_wcplus_

    def delete(self, l11l1l111l_wcplus_, a=False):
        """
        :param a: 是否需要删除公众号的昵称
        :param nick_name: 需要删除的微信昵称
        :return: 删除所有的参数
        """
        if l11l1l111l_wcplus_ == '?':
            a = True
        if a:
            l11l1l1ll1_wcplus_.delete()
            return
        l11l1l1ll1_wcplus_.delete(key=l11l1l111l_wcplus_ + '.nick_name')
        l11l11llll_wcplus_ = None
        for l11l1l1111_wcplus_ in self.l1l11ll1l_wcplus_:
            if l11l1l1111_wcplus_['nick_name'] == l11l1l111l_wcplus_:
                l11l11llll_wcplus_ = l11l1l1111_wcplus_['wxuin']
                break

        if l11l11llll_wcplus_:
            l11l1l1ll1_wcplus_.delete(key={'$regex': l11l11llll_wcplus_ + '.*'})

    def check(self):
        """
        :return: 轮训数据源 检查参数的状态 怎么检查呢？
        方便周期性运行 不停检查：
        1. 参与采集微信的数量
        2. 各个参数的采集时间
        """
        pass