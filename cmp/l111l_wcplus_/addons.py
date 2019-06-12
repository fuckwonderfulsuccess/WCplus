# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\l111l_wcplus_\addons.py
"""
自定义mimproxy脚本 详细见 https://docs.mitmproxy.org/stable/addons-overview/
由于使用anyproxy的历史原因 这里会解析mitmproxy代理数据为anyproxy同样的格式
"""
import json
from utils.l11ll1111_wcplus_ import l11ll11ll1_wcplus_
from utils.base import logger, l1lll1111_wcplus_
from datetime import datetime
from instance import l11l1l1ll1_wcplus_
l11l11llll_wcplus_ = None
l1lll111111_wcplus_ = {'load_more':'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg', 
 'getappmsgext':'https://mp.weixin.qq.com/mp/getappmsgext?', 
 'appmsg_comment':'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment', 
 'content':'https://mp.weixin.qq.com/s?', 
 'home':'https://mp.weixin.qq.com/mp/profile_ext?action=home'}

def l1lll11ll11_wcplus_(key, value):
    l1lll111ll1_wcplus_ = str(value).replace("'", '"')
    data = {'id':key,  'key':key,  'time':datetime.now(),  'value':l1lll111ll1_wcplus_}
    l11l1l1ll1_wcplus_.insert('id', data)


class l1lll111l1l_wcplus_:
    """
    拦截url_filter中的请求参数 用wxuin.key.req的格式作为key name 存入数据库
    """

    @staticmethod
    def _1ll1llll1l_wcplus_(l1l1l1111_wcplus_):
        """
        :param req_data:
        :return: 微信特有 从cookie中解析出wxuin
        """
        l11l11llll_wcplus_ = 'UNK'
        if 'Cookie' in l1l1l1111_wcplus_['requestOptions']['headers']:
            cookie_dict = l11ll11ll1_wcplus_(l1l1l1111_wcplus_['requestOptions']['headers']['Cookie'], ';', '=')
        else:
            cookie_dict = l11ll11ll1_wcplus_(l1l1l1111_wcplus_['requestOptions']['headers']['cookie'], ';', '=')
        if 'wxuin' in cookie_dict:
            l11l11llll_wcplus_ = cookie_dict['wxuin']
        return l11l11llll_wcplus_

    def request(self, l1lll1111l1_wcplus_):
        pass

    def response(self, l1lll1111l1_wcplus_):
        global l11l11llll_wcplus_
        for key in l1lll111111_wcplus_:
            if l1lll111111_wcplus_[key] in l1lll1111l1_wcplus_.request.url:
                l1l1l1111_wcplus_, timestamp = l1lll111lll_wcplus_.l1lll1111ll_wcplus_(l1lll1111l1_wcplus_.request)
                if key == 'home':
                    l11l11llll_wcplus_ = self._1ll1llll1l_wcplus_(l1l1l1111_wcplus_)
                if l11l11llll_wcplus_ == 'UNK':
                    return
                key_name = '%s.%s.req' % (l11l11llll_wcplus_, key)
                l1lll11ll11_wcplus_(key_name, l1l1l1111_wcplus_)
                logger.debug(key_name)
            if key == 'getappmsgext':
                status_code, text = l1lll111lll_wcplus_.get_response(l1lll1111l1_wcplus_.response)
                l1lll11l1ll_wcplus_ = json.loads(text)
                l11l1l111l_wcplus_ = 'UNK'
                if 'nick_name' in l1lll11l1ll_wcplus_:
                    l11l1l111l_wcplus_ = l1lll11l1ll_wcplus_['nick_name']
                    if l11l1l111l_wcplus_ == 'UNK':
                        logger.debug('没能找到微信昵称 换一篇文章点击试试看 确保文章底部阅读数据出现')
                    else:
                        l1lll11ll11_wcplus_(l11l1l111l_wcplus_ + '.nick_name', l11l11llll_wcplus_)
            elif key == 'home':
                status_code, l1lll11lll1_wcplus_ = l1lll111lll_wcplus_.get_response(l1lll1111l1_wcplus_.response)
                l1lll11l1l1_wcplus_ = l1lll11lll1_wcplus_.split('var nickname = "')[1].split('" || ""')[0]
                logger.info('准备公众号:' + l1lll11l1l1_wcplus_)
                l1lll11ll11_wcplus_('current_nickname', l1lll11l1l1_wcplus_)


class l1lll111lll_wcplus_:
    """
    解析flow数据 成为anyrpoxy格式
    """

    @staticmethod
    def l1lll1111ll_wcplus_(request):
        """
        :param request:
        :return: 模拟anyrpoxy 格式化请求数据
        """
        l1l1l1111_wcplus_ = {}
        l1l1l1111_wcplus_['protocol'] = request.scheme
        l1l1l1111_wcplus_['url'] = request.url
        l1l1l1111_wcplus_['requestOptions'] = {}
        l1l1l1111_wcplus_['requestOptions']['headers'] = l1lll111lll_wcplus_.l1lll11llll_wcplus_(request.headers)
        l1l1l1111_wcplus_['requestOptions']['hostname'] = request.pretty_host
        l1l1l1111_wcplus_['requestOptions']['port'] = request.port
        l1l1l1111_wcplus_['requestOptions']['path'] = request.path
        l1l1l1111_wcplus_['requestOptions']['method'] = request.method
        l1l1l1111_wcplus_['requestData'] = request.text
        timestamp = int(request.timestamp_end * 1000)
        return (
         l1l1l1111_wcplus_, timestamp)

    @staticmethod
    def get_response(response):
        """
        :param response:
        :return: 返回响应码和响应体
        """
        return (
         response.status_code, response.text)

    @staticmethod
    def l1lll11llll_wcplus_(headers):
        l1lll11l111_wcplus_ = {}
        for i in headers.fields:
            l1lll11l111_wcplus_[str(i[0], 'utf-8')] = str(i[1], 'utf-8')

        if ':authority' in l1lll11l111_wcplus_:
            l1lll11l111_wcplus_.pop(':authority')
        return l1lll11l111_wcplus_