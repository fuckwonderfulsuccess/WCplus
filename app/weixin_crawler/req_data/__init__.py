# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\weixin_crawler\req_data\__init__.py
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
from instance import col_req_data

class ReqData:

    def __init__(self):
        self.req_data_list = []
        self.wx_req_data_list = []

    def clean(self):
        """
        进行数据的初步处理
        1. 从数据源获取原始数据
        2. 基本格式转化
        3. 添加部分字段
        """
        self.req_data_list = []
        raw_data_list = col_req_data.get()
        for rd in raw_data_list:
            item = {}
            item['key'] = rd['key']
            item['time'] = datetime.timestamp(rd['time'])
            if rd['value'][0] == '{':
                item['value'] = json.loads(rd['value'])
            else:
                item['value'] = rd['value']
            self.req_data_list.append(item)

    def tidy(self):
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
        wx_req_data_list = []
        wx_req_data_dict = {}
        for rd in self.req_data_list:
            item = {}
            if rd['key'] == 'current_nickname':
                nickname = rd['value']
            elif 'req' in rd['key']:
                keys = rd['key'].split('.')
                if keys[0] not in wx_req_data_dict:
                    wx_req_data_dict[keys[0]] = {}
                wx_req_data_dict[keys[0]][keys[1]] = rd['value']
                wx_req_data_dict[keys[0]][keys[1]]['time'] = rd['time']
            elif 'nick_name' in rd['key']:
                keys = rd['key'].split('.')
                if rd['value'] not in wx_req_data_dict:
                    wx_req_data_dict[rd['value']] = {}
                wx_req_data_dict[rd['value']]['nick_name'] = keys[0]

        for key in wx_req_data_dict:
            item = wx_req_data_dict[key]
            item['wxuin'] = key
            item['nickname'] = nickname
            wx_req_data_list.append(item)

        self.wx_req_data_list = wx_req_data_list
        return wx_req_data_list

    def delete(self, nick_name, a=False):
        """
        :param a: 是否需要删除公众号的昵称
        :param nick_name: 需要删除的微信昵称
        :return: 删除所有的参数
        """
        if nick_name == '?':
            a = True
        if a:
            col_req_data.delete()
            return
        col_req_data.delete(key=nick_name + '.nick_name')
        wxuin = None
        for wx in self.wx_req_data_list:
            if wx['nick_name'] == nick_name:
                wxuin = wx['wxuin']
                break

        if wxuin:
            col_req_data.delete(key={'$regex': wxuin + '.*'})

    def check(self):
        """
        :return: 轮训数据源 检查参数的状态 怎么检查呢？
        方便周期性运行 不停检查：
        1. 参与采集微信的数量
        2. 各个参数的采集时间
        """
        pass