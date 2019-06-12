# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\l1l1lllll_wcplus_\l1lll1_wcplus_.py
"""
历史文章列表爬虫 每次接到任务都新建一个对象 该对象负责处理所有的错误
并不是每次请求都需要重新获取参数
"""
import re, requests
from utils.base import l1lll1111_wcplus_, logger
from utils.l11ll1111_wcplus_ import l11llll11_wcplus_
import json
from datetime import datetime

class l11lll1l1l_wcplus_:

    def __init__(self, offset, l11lll1ll1_wcplus_):
        """
        :param offset: 文章列表的offset
        :param wx_req_data: 一个微信的全部请求参数 也就是 wx_req_data_list中的一个
        :return 维护一个请求的请求参数和响应
        """
        self.req = {}
        self.res = {}
        self.offset = offset
        self.l11lll1ll1_wcplus_ = l11lll1ll1_wcplus_
        self.timeout = 10
        self.success = False

    def l11llll1ll_wcplus_(self):
        """
        :return: 结合offset和wx_req_data整理出请求需要的数据
        1. 正则表达式修改 url参数中的offset
        """
        rd = self.l11lll1ll1_wcplus_['load_more']
        self.req['url'] = re.sub('offset=\\d+', 'offset=%d' % self.offset, rd['url'])
        self.req['headers'] = rd['requestOptions']['headers']

    def l1ll1ll11l_wcplus_(self):
        """
        :return: 执行请求
        1. 发起请求
        2. 捕捉异常或再次请求
        3. 返回结果
        """
        resp = None
        l11lllll11_wcplus_ = 0
        while not resp:
            if l11lllll11_wcplus_ >= 3:
                logger.warning('获取历史文章列表发生错误%s 次数太多 放弃' % self.offset)
                break
                try:
                    resp = requests.get(url=self.req['url'],
                      headers=self.req['headers'],
                      timeout=self.timeout,
                      verify=True)
                except Exception as e:
                    l11lllll11_wcplus_ += 1
                    logger.warning('获取历史文章列表发生错误%s %s' % (self.offset, str(e)))

        return resp

    def l1ll1l1lll_wcplus_(self, resp):
        """
        :param resp: 请求的原始返回结果
        :return: 判断请求是否成功 如果不成功 直接采集相关措施
        1. 请求结果判断如果不是有效响应则再次发起请求
        2. 有可能需要更新参数
        """
        l11llllll1_wcplus_ = resp.json()
        if l11llllll1_wcplus_['errmsg'] == 'ok':
            self.success = True
            return resp
        self.success = False
        logger.error('获取历史文章列表参数过期或微信被限制%s' % l11llllll1_wcplus_)
        return

    def l1ll1ll111_wcplus_(self, resp):
        """
        :return: 解析响应返回成为原始数据
        1. 解析请求返回的结果
        """
        l1l11111ll_wcplus_ = l11lll11l1_wcplus_.l11llll11l_wcplus_(self.l11lll1ll1_wcplus_['nickname'], resp)
        return l1l11111ll_wcplus_

    def run(self):
        """
        :return: 返回结果
        """
        self.l11llll1ll_wcplus_()
        resp = self.l1ll1l1lll_wcplus_(self.l1ll1ll11l_wcplus_())
        if self.success:
            l1l11111ll_wcplus_ = self.l1ll1ll111_wcplus_(resp)
            return l1l11111ll_wcplus_
        return 'req_data_error'


class l11lll11l1_wcplus_:
    """
    解析获取文章列表
    """

    @staticmethod
    def l11llll11l_wcplus_(nickname, response):
        """
        :param response:请求返回的response
        :return:提取历史文章列表信息并且分类主副 主文章是一次推送的头条消息用10表示 其余文章从11开始表示
            r['r']['data']: title,digest,content_url,source_url,cover,author,mov,p_date,id
            r['r']['des']: can_msg_continue,next_offset
        """
        l11lll1lll_wcplus_ = {}
        l11lll1lll_wcplus_['data'] = []
        l11lll1lll_wcplus_['des'] = {}
        l11lll1lll_wcplus_['index'] = 0
        data = response.json()
        l11lll1lll_wcplus_['des']['can_msg_continue'] = data['can_msg_continue']
        l11lll1lll_wcplus_['des']['next_offset'] = data['next_offset']
        data = l11lll11l1_wcplus_.l11lllll1l_wcplus_(data.get('general_msg_list'))
        for msg in data:
            l1l1111111_wcplus_ = msg.get('comm_msg_info').get('datetime')
            l1l111111l_wcplus_ = msg.get('app_msg_ext_info')
            if l1l111111l_wcplus_:
                mov = 10
                l1l111111l_wcplus_['mov'] = str(mov)
                l1l111111l_wcplus_['nickname'] = nickname
                l11lll11l1_wcplus_._insert(l11lll1lll_wcplus_, l1l111111l_wcplus_, l1l1111111_wcplus_)
                l11lllllll_wcplus_ = l1l111111l_wcplus_.get('multi_app_msg_item_list')
                for l11llll1l1_wcplus_ in l11lllllll_wcplus_:
                    mov += 1
                    l11llll1l1_wcplus_['mov'] = str(mov)
                    l11llll1l1_wcplus_['nickname'] = nickname
                    l11lll11l1_wcplus_._insert(l11lll1lll_wcplus_, l11llll1l1_wcplus_, l1l1111111_wcplus_)

                continue

        l11lll1lll_wcplus_.pop('index')
        return l11lll1lll_wcplus_

    @staticmethod
    def l11lllll1l_wcplus_(l11lll1l11_wcplus_):
        l1l11111l1_wcplus_ = l11lll1l11_wcplus_.replace('\\/', '/')
        data = json.loads(l1l11111l1_wcplus_)
        return data.get('list')

    @staticmethod
    def _insert(l11lll1lll_wcplus_, item, l1l1111111_wcplus_):
        """
        文章列表信息插入use_data
        """
        l11lll1lll_wcplus_['index'] += 1
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url',
                'mov', 'nickname')
        l11lll11ll_wcplus_ = l11lll11l1_wcplus_.l11llll111_wcplus_(item, keys)
        l1l1111111_wcplus_ = datetime.fromtimestamp(l1l1111111_wcplus_)
        l11lll11ll_wcplus_['p_date'] = l1l1111111_wcplus_
        l11lll11ll_wcplus_['id'] = l11llll11_wcplus_(l11lll11ll_wcplus_['content_url'])
        l11lll11ll_wcplus_['mov'] = int(l11lll11ll_wcplus_['mov'])
        if l11lll11ll_wcplus_['title']:
            l11lll1lll_wcplus_['data'].append(l11lll11ll_wcplus_)
        item = {}
        item['style'] = '采集文章列表'
        item['nickname'] = l11lll11ll_wcplus_['nickname']
        item['process'] = l11lll1lll_wcplus_['index']
        item['data'] = l11lll11ll_wcplus_['mov']
        item['task'] = l11lll11ll_wcplus_['title'][:5] + '...'
        logger.info('采集文章列表中... %2d %2s %s' % (l11lll1lll_wcplus_['index'], l11lll11ll_wcplus_['mov'], l11lll11ll_wcplus_['title']))

    @staticmethod
    def l11llll111_wcplus_(d, keys):
        import html
        return {k:html.unescape(d[k]) for k in d if k in keys}