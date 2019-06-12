# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\l1ll1l1l1_wcplus_\__init__.py
"""
调度和管理爬虫采集一个公众号中所有没有阅读数据的文章
"""
from instance import rd
from utils.base import logger, l1lll1111_wcplus_
from utils.l11ll1111_wcplus_ import l11llll11_wcplus_
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
import time
from instance import l11ll11lll_wcplus_
from app.l1ll11ll1_wcplus_.l1ll1l1l1_wcplus_.l1lll1_wcplus_ import l11lll1l1l_wcplus_

class l1l1ll11l_wcplus_:

    def __init__(self):
        self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
        self.nickname = self.l1l11ll1l_wcplus_[0]['nickname']
        self.l11ll1l1ll_wcplus_ = 3.0
        self.l11ll1l111_wcplus_ = len(self.l1l11ll1l_wcplus_)
        self.delay = round(self.l11ll1l1ll_wcplus_ / self.l11ll1l111_wcplus_, 3)
        self.l11lll11l_wcplus_ = []
        self.l11ll111l_wcplus_ = l1l11llll_wcplus_(self.nickname)
        self.l11ll1lll1_wcplus_ = time.time()

    def l1l1l1l11_wcplus_(self, process=None, mov=10):
        """
        :param mov: 10~17
        :return: 轮流调用wx_req_data_list中的微信参数 采集文章的阅读数据
        """
        if 'getappmsgext' in self.l1l11ll1l_wcplus_[0]:
            l11l1ll11l_wcplus_ = self.l11ll111l_wcplus_.table.find({'$and': [{'read_num': {'$exists': False}}, {'mov': {'$lte': int(mov)}}]})
            cnt = 0
            for a in l11l1ll11l_wcplus_:
                if 'mp.weixin.qq.com' in a['content_url']:
                    if 'comment_id' not in a:
                        a['comment_id'] = 0
                    self.l11lll11l_wcplus_.append([cnt, a['content_url'], a['comment_id']])
                    cnt += 1

            for l11l1ll111_wcplus_ in self.l11lll11l_wcplus_:
                while time.time() - self.l11ll1lll1_wcplus_ <= self.delay:
                    time.sleep(0.05)

                self.l11ll1lll1_wcplus_ = time.time()
                l1ll1l1l1_wcplus_ = l11lll1l1l_wcplus_(l11l1ll111_wcplus_[1], l11l1ll111_wcplus_[2], self.l1l11ll1l_wcplus_[l11l1ll111_wcplus_[0] % self.l11ll1l111_wcplus_]).run()
                l1ll1l1l1_wcplus_ = self.check(l1ll1l1l1_wcplus_, l11l1ll111_wcplus_)
                l1ll1l1l1_wcplus_['id'] = l11llll11_wcplus_(l11l1ll111_wcplus_[1])
                self.l11ll111l_wcplus_.insert('id', l1ll1l1l1_wcplus_)
                process.l11l1lll1_wcplus_(l11l1ll111_wcplus_[0] + 1, len(self.l11lll11l_wcplus_), self.delay)

        else:
            logger.warning('点击查看该公众号的任意一篇文章且出现阅读量')

    def save(self, l1ll1l1l1_wcplus_):
        """
        :param reading_data:
        :return: 保存数据
        """
        pass

    def l11111l11_wcplus_(self):
        """
        :return: 多线程的方式准备任务
        """
        for item in self.l11lll11l_wcplus_:
            yield {'index':item[0], 
             'url':item[1]}

    def l1llllll1l_wcplus_(self, task):
        """
        :return: 多线程的方式任务处理器
        """
        l11lll1l1l_wcplus_(task['url'], self.l1l11ll1l_wcplus_[task['index'] % self.l11ll1l111_wcplus_]).run()

    def check(self, l1ll1l1l1_wcplus_, item):
        """
        :return: 带着本次请求的参数和结果一起过安检
        请求失败导致安检不通过 安检提醒人重新操作手机 操作完之后再次发起请求
        不排除还是会失败  继续调用自己 反正想办法让其获得成功的请求  最后返回成功的请求
        """
        if l1ll1l1l1_wcplus_ != 'req_data_error':
            l11ll11lll_wcplus_.check({'crawler':'阅读数据',  'msg':'success'})
        else:
            l11ll11lll_wcplus_.check({'crawler':'阅读数据',  'msg':'req_data_error'})
            self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
            while len(self.l1l11ll1l_wcplus_) == 0:
                self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
                from utils.front import l1l11111l_wcplus_
                l1l11111l_wcplus_('没有发现参数', '参数错误', _type='error')
                time.sleep(3)

            l1ll1l1l1_wcplus_ = l11lll1l1l_wcplus_(item[1], item[2], self.l1l11ll1l_wcplus_[0]).run()
            self.check(l1ll1l1l1_wcplus_, item)
        return l1ll1l1l1_wcplus_