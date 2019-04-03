# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\weixin_crawler\article_list\crawler.py
"""
历史文章列表爬虫 每次接到任务都新建一个对象 该对象负责处理所有的错误
并不是每次请求都需要重新获取参数
"""
import re, requests
from utils.base import debug_p, logger
from utils.data_process import get_md5
import json
from datetime import datetime

class Crawler:

    def __init__(self, offset, wx_req_data):
        """
        :param offset: 文章列表的offset
        :param wx_req_data: 一个微信的全部请求参数 也就是 wx_req_data_list中的一个
        :return 维护一个请求的请求参数和响应
        """
        self.req = {}
        self.res = {}
        self.offset = offset
        self.wx_req_data = wx_req_data
        self.timeout = 10
        self.success = False

    def prepare_req_data(self):
        """
        :return: 结合offset和wx_req_data整理出请求需要的数据
        1. 正则表达式修改 url参数中的offset
        """
        rd = self.wx_req_data['load_more']
        self.req['url'] = re.sub('offset=\\d+', 'offset=%d' % self.offset, rd['url'])
        self.req['headers'] = rd['requestOptions']['headers']

    def act_request(self):
        """
        :return: 执行请求
        1. 发起请求
        2. 捕捉异常或再次请求
        3. 返回结果
        """
        resp = None
        proxy_err_cnt = 0
        while not resp:
            if proxy_err_cnt >= 3:
                logger.warning('获取历史文章列表发生错误%s 次数太多 放弃' % self.offset)
                break
                try:
                    resp = requests.get(url=self.req['url'],
                      headers=self.req['headers'],
                      timeout=self.timeout,
                      verify=True)
                except Exception as e:
                    proxy_err_cnt += 1
                    logger.warning('获取历史文章列表发生错误%s %s' % (self.offset, str(e)))

        return resp

    def jude_request(self, resp):
        """
        :param resp: 请求的原始返回结果
        :return: 判断请求是否成功 如果不成功 直接采集相关措施
        1. 请求结果判断如果不是有效响应则再次发起请求
        2. 有可能需要更新参数
        """
        resp_json = resp.json()
        if resp_json['errmsg'] == 'ok':
            self.success = True
            return resp
        self.success = False
        logger.error('获取历史文章列表参数过期或微信被限制%s' % resp_json)
        return

    def decode_response(self, resp):
        """
        :return: 解析响应返回成为原始数据
        1. 解析请求返回的结果
        """
        list_data = DecodeArticleList.decode_load_more(self.wx_req_data['nickname'], resp)
        return list_data

    def run(self):
        """
        :return: 返回结果
        """
        self.prepare_req_data()
        resp = self.jude_request(self.act_request())
        if self.success:
            list_data = self.decode_response(resp)
            return list_data
        return 'req_data_error'


class DecodeArticleList:
    """
    解析获取文章列表
    """

    @staticmethod
    def decode_load_more(nickname, response):
        """
        :param response:请求返回的response
        :return:提取历史文章列表信息并且分类主副 主文章是一次推送的头条消息用10表示 其余文章从11开始表示
            r['r']['data']: title,digest,content_url,source_url,cover,author,mov,p_date,id
            r['r']['des']: can_msg_continue,next_offset
        """
        use_data = {}
        use_data['data'] = []
        use_data['des'] = {}
        use_data['index'] = 0
        data = response.json()
        use_data['des']['can_msg_continue'] = data['can_msg_continue']
        use_data['des']['next_offset'] = data['next_offset']
        data = DecodeArticleList.general_msg_list_to_list(data.get('general_msg_list'))
        for msg in data:
            p_date = msg.get('comm_msg_info').get('datetime')
            msg_info = msg.get('app_msg_ext_info')
            if msg_info:
                mov = 10
                msg_info['mov'] = str(mov)
                msg_info['nickname'] = nickname
                DecodeArticleList._insert(use_data, msg_info, p_date)
                multi_msg_info = msg_info.get('multi_app_msg_item_list')
                for msg_item in multi_msg_info:
                    mov += 1
                    msg_item['mov'] = str(mov)
                    msg_item['nickname'] = nickname
                    DecodeArticleList._insert(use_data, msg_item, p_date)

                continue

        use_data.pop('index')
        return use_data

    @staticmethod
    def general_msg_list_to_list(general_msg_list):
        msg_list = general_msg_list.replace('\\/', '/')
        data = json.loads(msg_list)
        return data.get('list')

    @staticmethod
    def _insert(use_data, item, p_date):
        """
        文章列表信息插入use_data
        """
        use_data['index'] += 1
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url',
                'mov', 'nickname')
        sub_data = DecodeArticleList.sub_dict(item, keys)
        p_date = datetime.fromtimestamp(p_date)
        sub_data['p_date'] = p_date
        sub_data['id'] = get_md5(sub_data['content_url'])
        if sub_data['title']:
            use_data['data'].append(sub_data)
        item = {}
        item['style'] = '采集文章列表'
        item['nickname'] = sub_data['nickname']
        item['process'] = use_data['index']
        item['data'] = sub_data['mov']
        item['task'] = sub_data['title'][:5] + '...'
        logger.info('采集文章列表中... %2d %2s %s' % (use_data['index'], sub_data['mov'], sub_data['title']))

    @staticmethod
    def sub_dict(d, keys):
        import html
        return {k:html.unescape(d[k]) for k in d if k in keys}