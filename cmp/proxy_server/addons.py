# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\proxy_server\addons.py
"""
自定义mimproxy脚本 详细见 https://docs.mitmproxy.org/stable/addons-overview/
由于使用anyproxy的历史原因 这里会解析mitmproxy代理数据为anyproxy同样的格式
"""
import json
from utils.data_process import str_to_dict
from utils.base import logger, debug_p
from datetime import datetime
from instance import col_req_data
url_filter = {'load_more':'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg', 
 'getappmsgext':'https://mp.weixin.qq.com/mp/getappmsgext?', 
 'appmsg_comment':'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment', 
 'content':'https://mp.weixin.qq.com/s?', 
 'home':'https://mp.weixin.qq.com/mp/profile_ext?action=home'}

def insert_helper(key, value):
    json_value = str(value).replace("'", '"')
    data = {'id':key,  'key':key,  'time':datetime.now(),  'value':json_value}
    col_req_data.insert('id', data)


class SelfAddon:
    """
    拦截url_filter中的请求参数 用wxuin.key.req的格式作为key name 存入数据库
    """

    @staticmethod
    def _extract_wxuin(req_data):
        """
        :param req_data:
        :return: 微信特有 从cookie中解析出wxuin
        """
        wxuin = 'UNK'
        cookie_dict = str_to_dict(req_data['requestOptions']['headers']['Cookie'], ';', '=')
        if 'wxuin' in cookie_dict:
            wxuin = cookie_dict['wxuin']
        return wxuin

    def request(self, flow):
        pass

    def response(self, flow):
        for key in url_filter:
            if url_filter[key] in flow.request.url:
                req_data, timestamp = ExtractFlow.format_request_data(flow.request)
                wxuin = self._extract_wxuin(req_data)
                if wxuin == 'UNK':
                    return
                key_name = '%s.%s.req' % (wxuin, key)
                insert_helper(key_name, req_data)
                logger.debug(key_name)
            if key == 'getappmsgext':
                status_code, text = ExtractFlow.get_response(flow.response)
                text_dict = json.loads(text)
                nick_name = 'UNK'
                if 'nick_name' in text_dict:
                    nick_name = text_dict['nick_name']
                    if nick_name == 'UNK':
                        logger.debug('没能找到微信昵称 换一篇文章点击试试看 确保文章底部阅读数据出现')
                    else:
                        insert_helper(nick_name + '.nick_name', wxuin)
            elif key == 'home':
                status_code, html_text = ExtractFlow.get_response(flow.response)
                current_nickname = html_text.split('var nickname = "')[1].split('" || ""')[0]
                logger.info('准备公众号:' + current_nickname)
                insert_helper('current_nickname', current_nickname)


class ExtractFlow:
    """
    解析flow数据 成为anyrpoxy格式
    """

    @staticmethod
    def format_request_data(request):
        """
        :param request:
        :return: 模拟anyrpoxy 格式化请求数据
        """
        req_data = {}
        req_data['protocol'] = request.scheme
        req_data['url'] = request.url
        req_data['requestOptions'] = {}
        req_data['requestOptions']['headers'] = ExtractFlow.decode_headers(request.headers)
        req_data['requestOptions']['hostname'] = request.pretty_host
        req_data['requestOptions']['port'] = request.port
        req_data['requestOptions']['path'] = request.path
        req_data['requestOptions']['method'] = request.method
        req_data['requestData'] = request.text
        timestamp = int(request.timestamp_end * 1000)
        return (
         req_data, timestamp)

    @staticmethod
    def get_response(response):
        """
        :param response:
        :return: 返回响应码和响应体
        """
        return (
         response.status_code, response.text)

    @staticmethod
    def decode_headers(headers):
        headers_data = {}
        for i in headers.fields:
            headers_data[str(i[0], 'utf-8')] = str(i[1], 'utf-8')

        return headers_data