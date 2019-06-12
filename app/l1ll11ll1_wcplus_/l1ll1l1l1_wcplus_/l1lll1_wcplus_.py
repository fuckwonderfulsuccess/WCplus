# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\l1ll1l1l1_wcplus_\l1lll1_wcplus_.py
"""
阅读数据爬虫
"""
import requests
from utils.base import l1lll1111_wcplus_, logger
from copy import copy
from datetime import datetime
from utils.l11ll1111_wcplus_ import l11ll11ll1_wcplus_, l11l1ll1ll_wcplus_, l11ll111l1_wcplus_
import time
from instance import l11ll11lll_wcplus_

class l11lll1l1l_wcplus_:

    def __init__(self, url, comment_id, l11lll1ll1_wcplus_):
        """
        :param url: 文章的url
        :param wx_req_data: 一个微信的全部请求参数 也就是 wx_req_data_list中的一个
        :return 维护一个请求的请求参数和响应
        """
        self.req = {}
        self.res = {}
        self.url = url
        self.comment_id = comment_id
        self.l11lll1ll1_wcplus_ = l11lll1ll1_wcplus_
        self.timeout = 20
        self.success = False

    @staticmethod
    def l11l1lllll_wcplus_(l11l1lll11_wcplus_):
        """
        :param url_parm_dict:
        :return: 重命名微信文章链接参数名称
        """
        l11l1lll1l_wcplus_ = {'__biz':'__biz', 
         'mid':'mid', 
         'idx':'idx', 
         'scene':'scene', 
         'sn':'sn', 
         'appmsgid':'mid', 
         'itemidx':'idx', 
         'sign':'sn', 
         'chksm':'chksm'}
        l11ll11l1l_wcplus_ = copy(l11l1lll11_wcplus_)
        for key in l11l1lll11_wcplus_:
            l11ll11l1l_wcplus_[l11l1lll1l_wcplus_[key]] = l11ll11l1l_wcplus_.pop(key)

        return l11ll11l1l_wcplus_

    def l11llll1ll_wcplus_(self):
        """
        :return: 根据url整理请求参数
        """
        rd = self.l11lll1ll1_wcplus_['getappmsgext']
        l11l1lll11_wcplus_ = l11ll11ll1_wcplus_(self.url.split('?')[1], '&', '=')
        l11ll11111_wcplus_ = l11ll11ll1_wcplus_(rd['requestData'], '&', '=')
        l11ll1111l_wcplus_ = self.l11l1lllll_wcplus_(l11l1lll11_wcplus_)
        l11ll11111_wcplus_['is_need_reward'] = 1
        l11ll111l1_wcplus_(l11ll11111_wcplus_, l11ll1111l_wcplus_, ['mid', 'sn', 'idx', 'scene'])
        l11ll11111_wcplus_['comment_id'] = self.comment_id
        l11ll11111_wcplus_['is_need_reward'] = 1
        self.req['url'] = rd['url']
        self.req['body'] = l11l1ll1ll_wcplus_(l11ll11111_wcplus_)
        self.req['headers'] = rd['requestOptions']['headers']

    def l1ll1ll11l_wcplus_(self):
        """
        :return: 执行请求 如果请求失败返回字符串"error"
        """
        resp = None
        l11lllll11_wcplus_ = 0
        while not resp:
            if l11lllll11_wcplus_ >= 3:
                logger.warning('获取历史文章阅读数据发生错误%s 次数太多 放弃' % self.url)
                return 'error'
                try:
                    resp = requests.post(url=self.req['url'],
                      data=self.req['body'],
                      headers=self.req['headers'],
                      timeout=self.timeout,
                      verify=True)
                except Exception as e:
                    l11lllll11_wcplus_ += 1
                    logger.warning('获取文章阅读数据发生错误 5秒钟之后再次尝试 %s %s' % (self.url, str(e)))
                    time.sleep(5)

        return resp

    def l1ll1l1lll_wcplus_(self, resp):
        """
        :return: 判断请求是否成功 如果不成功 直接采集相关措施
        比如重新请求 或者操作手机获取参数
        """
        if resp == 'error':
            logger.error('请求失败, 未能获取到阅读数据')
            self.success = False
            return
        l11llllll1_wcplus_ = resp.json()
        if 'appmsgstat' in l11llllll1_wcplus_:
            l11ll11lll_wcplus_.check({'crawler':'阅读数据',  'msg':'success'})
            self.success = True
            return resp
        logger.error('请求阅读数据参数错误 %s' % self.url)
        self.success = False
        return

    def l1ll1ll111_wcplus_(self, resp):
        """
        :return: 解析响应返回成为原始数据
        """
        read_data = l11ll111ll_wcplus_.l11l1ll1l1_wcplus_(resp)
        return read_data

    def run(self):
        """
        :return: 运行所有的过程
        """
        self.l11llll1ll_wcplus_()
        resp = self.l1ll1l1lll_wcplus_(self.l1ll1ll11l_wcplus_())
        if self.success:
            read_data = self.l1ll1ll111_wcplus_(resp)
            return read_data
        return 'req_data_error'


class l11ll111ll_wcplus_:

    @staticmethod
    def l11l1ll1l1_wcplus_(response):
        l11ll11l11_wcplus_ = response.json()
        read_data = {}
        read_data['read_num'] = l11ll11l11_wcplus_.get('appmsgstat').get('read_num')
        read_data['like_num'] = l11ll11l11_wcplus_.get('appmsgstat').get('like_num')
        read_data['reward_num'] = l11ll11l11_wcplus_.get('reward_total_count')
        if read_data['read_num'] is None:
            read_data['read_num'] = -2
        if read_data['like_num'] is None:
            read_data['like_num'] = -2
        if read_data['reward_num'] is None:
            read_data['reward_num'] = -2
        read_data['c_date'] = datetime.now()
        read_data['comment_num'] = l11ll11l11_wcplus_.get('comment_count')
        if read_data['comment_num'] is None:
            read_data['comment_num'] = -2
        l11ll111ll_wcplus_.l11l1llll1_wcplus_(read_data)
        return read_data

    @staticmethod
    def l11l1llll1_wcplus_(rd):
        logger.info('采集阅读数据中... 阅读%-5d 点赞%-4d 赞赏%3d 评论%d' % (rd['read_num'], rd['like_num'], rd['reward_num'], rd['comment_num']))