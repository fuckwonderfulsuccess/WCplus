# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\l1ll11ll1_wcplus_\l1l1lllll_wcplus_\__init__.py
"""
调度和管理爬虫 采集完成一个公众号的全部历史文章列表
"""
from app.l1ll11ll1_wcplus_.l1l1lllll_wcplus_.l1lll1_wcplus_ import l11lll1l1l_wcplus_
from instance import rd, l1l1l11l1_wcplus_
from cmp.db.l1ll11l11_wcplus_ import l1l11llll_wcplus_
from utils.base import logger, l1lll1111_wcplus_
from datetime import datetime
from instance import l11ll11lll_wcplus_
import time

class l1ll11111_wcplus_:
    """
    优雅地拿下一个公众号的全部历史文章列表
    如果有必要直接调用自动操作手机的方法
    采集完毕之后结束对象的生命周期
    """

    def __init__(self):
        self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
        self.nickname = self.l1l11ll1l_wcplus_[0]['nickname']
        self.l11ll1l1ll_wcplus_ = 2.0
        self.l11ll1l111_wcplus_ = len(self.l1l11ll1l_wcplus_)
        self.delay = round(self.l11ll1l1ll_wcplus_ / self.l11ll1l111_wcplus_, 3)
        self.l11ll11ll_wcplus_ = 0
        self.l11lll1111_wcplus_ = 0
        self.l11ll1ll1l_wcplus_ = []
        self.l11ll111l_wcplus_ = l1l11llll_wcplus_(self.nickname)
        self.l11ll1lll1_wcplus_ = time.time()

    def l1lll111l_wcplus_(self, filter=None, process=None):
        """
        :param filter: 过滤器比如按照时间过滤 按照数量过滤
        :param process: 前端进度显示实例
        :return: 轮流调用list中的微信 获取所有的历史文章列表
        """
        offset = 0
        l11ll1l11l_wcplus_ = 1
        cnt = 0
        if 'load_more' in self.l1l11ll1l_wcplus_[0]:
            while l11ll1l11l_wcplus_:
                while time.time() - self.l11ll1lll1_wcplus_ <= self.delay:
                    time.sleep(0.05)

                self.l11ll1lll1_wcplus_ = time.time()
                l1l11111ll_wcplus_ = l11lll1l1l_wcplus_(offset, self.l1l11ll1l_wcplus_[cnt % self.l11ll1l111_wcplus_]).run()
                l1l11111ll_wcplus_ = self.check(l1l11111ll_wcplus_, offset, cnt)
                l11ll1l11l_wcplus_ = int(l1l11111ll_wcplus_['des']['can_msg_continue'])
                offset = int(l1l11111ll_wcplus_['des']['next_offset'])
                cnt += 1
                self.l11ll1ll1l_wcplus_ = l1l11111ll_wcplus_['data']
                self.l11ll11ll_wcplus_ += len(self.l11ll1ll1l_wcplus_)
                l11lll111l_wcplus_ = self.l11ll1ll11_wcplus_(filter)
                self.l11lll1111_wcplus_ += len(self.l11ll1ll1l_wcplus_)
                l1l1l11l1_wcplus_.insert('id', {'id':self.nickname,  'num':self.l11lll1111_wcplus_,  'nickname':self.nickname,  'time':datetime.now()})
                process.l11l1ll1l_wcplus_(self.l11lll1111_wcplus_)
                if self.save(self.l11ll1ll1l_wcplus_) == 'UPDATE':
                    break
                if not l11lll111l_wcplus_:
                    break
                time.sleep(self.delay)

        else:
            logger.warning('没有上滑加载更多历史文章')

    def save(self, l1l11111ll_wcplus_):
        """
        :return: 保存数据
        """
        res = None
        res = self.l11ll111l_wcplus_.insert('id', l1l11111ll_wcplus_)
        return res

    def l11ll1ll11_wcplus_(self, filter):
        """
        :param filter:
        :return: 根据过滤器中的条件 决定继续还是结束文章列表的采集 True继续 false停止
        """
        if filter['type'] == 'true':
            if int(filter['num']) == 0:
                return True
            if self.l11ll11ll_wcplus_ >= int(filter['num']):
                return False
            return True
        else:
            l11ll1llll_wcplus_ = []
            res = True
            for a in self.l11ll1ll1l_wcplus_:
                l11ll1l1l1_wcplus_ = a['p_date'].timestamp()
                if l11ll1l1l1_wcplus_ >= filter['start_time'] and l11ll1l1l1_wcplus_ <= filter['end_time']:
                    l11ll1llll_wcplus_.append(a)
                elif l11ll1l1l1_wcplus_ < filter['start_time']:
                    res = False

            self.l11ll1ll1l_wcplus_ = l11ll1llll_wcplus_
            return res

    def check(self, l1l11111ll_wcplus_, offset, cnt):
        """
        :param list_data: 请求返回的结果
        :param offset:
        :return: 带着本次请求的参数和结果一起过安检
        请求失败导致安检不通过 安检提醒人重新操作手机 操作完之后再次发起请求
        不排除还是会失败  继续调用自己
        """
        if l1l11111ll_wcplus_ != 'req_data_error':
            l11ll11lll_wcplus_.check({'crawler':'历史文章列表',  'msg':'success'})
        else:
            l11ll11lll_wcplus_.check({'crawler':'历史文章列表',  'msg':'req_data_error'})
            self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
            while len(self.l1l11ll1l_wcplus_) == 0:
                self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()
                from utils.front import l1l11111l_wcplus_
                l1l11111l_wcplus_('没有发现参数', '参数错误', _type='error')
                time.sleep(3)

            l1l11111ll_wcplus_ = l11lll1l1l_wcplus_(offset, self.l1l11ll1l_wcplus_[0]).run()
            self.check(l1l11111ll_wcplus_, offset, cnt)
        return l1l11111ll_wcplus_