# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\l1lll1_wcplus_.py
"""
为采集页面提供数据和操作支持 整理符合前端显示格式的数据
"""
from instance import rd
from utils.base import l1lll1111_wcplus_
from l1l11_wcplus_ import socketio
from datetime import datetime
import time

class l1111_wcplus_:
    """
    为前端准备请求参数的显示
    """

    def __init__(self):
        self.l1l11ll1l_wcplus_ = rd.l1ll11l1l_wcplus_()

    def get(self):
        """
        :return: 所有的数据
        """
        data = []
        for l1l1111l1_wcplus_ in self.l1l11ll1l_wcplus_:
            item = {}
            item['more'] = '0'
            if 'load_more' in l1l1111l1_wcplus_:
                item['more'] = l1l1111l1_wcplus_['load_more']['time']
            item['reading'] = '0'
            if 'getappmsgext' in l1l1111l1_wcplus_:
                item['reading'] = l1l1111l1_wcplus_['getappmsgext']['time']
            item['nickname'] = '?'
            if 'nickname' in l1l1111l1_wcplus_:
                item['nickname'] = l1l1111l1_wcplus_['nickname']
            item['nick_name'] = '?'
            if 'nick_name' in l1l1111l1_wcplus_:
                item['nick_name'] = l1l1111l1_wcplus_['nick_name']
            data.append(item)

        return data

    def send(self):
        """
        :return: 通过websocket 发送数据到前端
        """
        socketio.emit('req_data', self.get())


def l1l1l11ll_wcplus_(nickname):
    from utils.front import l1l11111l_wcplus_
    l1l11111l_wcplus_('正在准备搜索工作 请不要关闭WCplus', nickname, 'warning')
    from app.search.index import l1l1lll1l_wcplus_
    l1l1lll1l_wcplus_(nickname).index()
    l1l11111l_wcplus_('可以开始搜索啦', nickname, 'success')


class l1l111l1l_wcplus_:
    """
    接受采集范围作为参数 从数据库中读取请求参数执行采集任务
    """

    def __init__(self, filter):
        if filter['start_time']:
            filter['start_time'] = datetime.strptime(filter['start_time'].split('T')[0], '%Y-%m-%d').timestamp()
            filter['end_time'] = datetime.strptime(filter['end_time'].split('T')[0], '%Y-%m-%d').timestamp()
        self.filter = filter
        self.begin_time = time.time()

    def l1l1ll1l1_wcplus_(self, process):
        """
        :return: 根据数请求参数发起一次文章列表采集
        """
        from app.l1ll11ll1_wcplus_.l1l1lllll_wcplus_ import l1ll11111_wcplus_
        l1ll1l1ll_wcplus_ = l1ll11111_wcplus_()
        l1ll1l1ll_wcplus_.l1lll111l_wcplus_(filter=self.filter, process=process)

    def l1ll1ll11_wcplus_(self, process, mov):
        """
        :return: 根据请求参数发起一次阅读数据采集
        """
        from app.l1ll11ll1_wcplus_.l1ll1l1l1_wcplus_ import l1l1ll11l_wcplus_
        l1l1llll1_wcplus_ = l1l1ll11l_wcplus_()
        l1l1llll1_wcplus_.l1l1l1l11_wcplus_(process, mov=mov)

    def l1ll1l111_wcplus_(self, process):
        """
        :return: 根据请求参数发起一次文章内容采集
        """
        from instance import l1l1111ll_wcplus_
        l1l11l11l_wcplus_ = l1l1111ll_wcplus_.get()['use_proxy']
        if l1l11l11l_wcplus_ == 'false':
            l1ll11lll_wcplus_ = 64
        else:
            l1ll11lll_wcplus_ = 8
        l1lll1111_wcplus_(l1ll11lll_wcplus_)
        from app.l1ll11ll1_wcplus_.article import l1l1ll1ll_wcplus_
        l1l1ll1ll_wcplus_(l1ll11lll_wcplus_=l1ll11lll_wcplus_, process=process)

    @staticmethod
    def l1l111l11_wcplus_(al):
        """
        :return: 将前端的article_location转化为mov
        """
        mov = int(al / 10) + 10
        if mov > 17:
            mov = 17
        return mov

    def l1l11l1ll_wcplus_(self):
        from utils.front import l1l111lll_wcplus_
        from cmp.protect import Passport
        if not Passport.l1l11l111_wcplus_():
            l1l111lll_wcplus_('请先通过使用说明书中的方法获得授权有效授权证书', '授权无效 不可采集数据', 'error')
            return
        l1l11ll11_wcplus_ = rd.l1ll11l1l_wcplus_()
        if len(l1l11ll11_wcplus_) == 0:
            return
        nickname = l1l11ll11_wcplus_[0]['nickname']
        from app.api.process import Process
        l1l111ll1_wcplus_ = int(self.filter['range'])
        mov = self.l1l111l11_wcplus_(int(self.filter['article_location']))
        process = Process(l1l111ll1_wcplus_)
        import builtins
        builtins.crawler_process = process
        if l1l111ll1_wcplus_ == 0:
            process.new_step()
            self.l1l1ll1l1_wcplus_(process)
            l1l1l11ll_wcplus_(nickname)
        else:
            if l1l111ll1_wcplus_ == 25:
                process.new_step()
                self.l1l1ll1l1_wcplus_(process)
                process.new_step()
                self.l1ll1l111_wcplus_(process)
                l1l1l11ll_wcplus_(nickname)
            else:
                if l1l111ll1_wcplus_ == 50:
                    process.new_step()
                    self.l1l1ll1l1_wcplus_(process)
                    l1l1l11ll_wcplus_(nickname)
                    process.new_step()
                    self.l1ll1ll11_wcplus_(process, mov)
                else:
                    if l1l111ll1_wcplus_ == 75:
                        process.new_step()
                        self.l1l1ll1l1_wcplus_(process)
                        process.new_step()
                        self.l1ll1l111_wcplus_(process)
                        l1l1l11ll_wcplus_(nickname)
                        process.new_step()
                        self.l1ll1ll11_wcplus_(process, mov)
                    else:
                        if l1l111ll1_wcplus_ == 100:
                            process.new_step()
                            self.l1ll1ll11_wcplus_(process, mov)
        process.l1l11l1l1_wcplus_()
        l1l111lll_wcplus_('总共用时%d分钟' % int((time.time() - self.begin_time) / 60), '采集完成', 'success')