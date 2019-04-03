# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\weixin_crawler\article_list\__init__.py
"""
调度和管理爬虫 采集完成一个公众号的全部历史文章列表
"""
from app.weixin_crawler.article_list.crawler import Crawler
from instance import rd, col_crawler_log
from cmp.db.mongo import CollectionOperation
from utils.base import logger, debug_p
from datetime import datetime
from instance import stop_and_start
import time

class AricleList:
    """
    优雅地拿下一个公众号的全部历史文章列表
    如果有必要直接调用自动操作手机的方法
    采集完毕之后结束对象的生命周期
    """

    def __init__(self):
        self.wx_req_data_list = rd.tidy()
        self.nickname = self.wx_req_data_list[0]['nickname']
        self.every_delay = 2.0
        self.wx_num = len(self.wx_req_data_list)
        self.delay = round(self.every_delay / self.wx_num, 3)
        self.article_num = 0
        self.all_article_num = 0
        self.current_article_list = []
        self.col_data = CollectionOperation(self.nickname)
        self.pre_crawl_time = time.time()

    def get_all_article_list(self, filter=None, process=None):
        """
        :param filter: 过滤器比如按照时间过滤 按照数量过滤
        :param process: 前端进度显示实例
        :return: 轮流调用list中的微信 获取所有的历史文章列表
        """
        offset = 0
        can_msg_continue = 1
        cnt = 0
        if 'load_more' in self.wx_req_data_list[0]:
            while can_msg_continue:
                while time.time() - self.pre_crawl_time <= self.delay:
                    time.sleep(0.05)

                self.pre_crawl_time = time.time()
                list_data = Crawler(offset, self.wx_req_data_list[cnt % self.wx_num]).run()
                list_data = self.check(list_data, offset, cnt)
                can_msg_continue = int(list_data['des']['can_msg_continue'])
                offset = int(list_data['des']['next_offset'])
                cnt += 1
                self.current_article_list = list_data['data']
                self.article_num += len(self.current_article_list)
                filter_res = self.filter_check(filter)
                self.all_article_num += len(self.current_article_list)
                col_crawler_log.insert('id', {'id':self.nickname,  'num':self.all_article_num,  'nickname':self.nickname,  'time':datetime.now()})
                process.new_article_list(self.all_article_num)
                if self.save(self.current_article_list) == 'UPDATE':
                    break
                if not filter_res:
                    break
                time.sleep(self.delay)

        else:
            logger.warning('没有上滑加载更多历史文章')

    def save(self, list_data):
        """
        :return: 保存数据
        """
        res = None
        res = self.col_data.insert('id', list_data)
        return res

    def filter_check(self, filter):
        """
        :param filter:
        :return: 根据过滤器中的条件 决定继续还是结束文章列表的采集 True继续 false停止
        """
        if filter['type'] == 'true':
            if int(filter['num']) == 0:
                return True
            if self.article_num >= int(filter['num']):
                return False
            return True
        else:
            use_article_list = []
            res = True
            for a in self.current_article_list:
                p_date_timestamp = a['p_date'].timestamp()
                if p_date_timestamp >= filter['start_time'] and p_date_timestamp <= filter['end_time']:
                    use_article_list.append(a)
                elif p_date_timestamp < filter['start_time']:
                    res = False

            self.current_article_list = use_article_list
            return res

    def check(self, list_data, offset, cnt):
        """
        :param list_data: 请求返回的结果
        :param offset:
        :return: 带着本次请求的参数和结果一起过安检
        请求失败导致安检不通过 安检提醒人重新操作手机 操作完之后再次发起请求
        不排除还是会失败  继续调用自己
        """
        if list_data != 'req_data_error':
            stop_and_start.check({'crawler':'历史文章列表',  'msg':'success'})
        else:
            stop_and_start.check({'crawler':'历史文章列表',  'msg':'req_data_error'})
            self.wx_req_data_list = rd.tidy()
            while len(self.wx_req_data_list) == 0:
                self.wx_req_data_list = rd.tidy()
                from utils.front import notification
                notification('没有发现参数', '参数错误', _type='error')
                time.sleep(3)

            list_data = Crawler(offset, self.wx_req_data_list[0]).run()
            self.check(list_data, offset, cnt)
        return list_data