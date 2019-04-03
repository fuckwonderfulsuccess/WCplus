# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\weixin_crawler\reading_data\__init__.py
"""
调度和管理爬虫采集一个公众号中所有没有阅读数据的文章
"""
from instance import rd
from utils.base import logger, debug_p
from utils.data_process import get_md5
from cmp.db.mongo import CollectionOperation
import time
from instance import stop_and_start
from app.weixin_crawler.reading_data.crawler import Crawler

class ReadingData:

    def __init__(self):
        self.wx_req_data_list = rd.tidy()
        self.nickname = self.wx_req_data_list[0]['nickname']
        self.every_delay = 3.0
        self.wx_num = len(self.wx_req_data_list)
        self.delay = round(self.every_delay / self.wx_num, 3)
        self.articles = []
        self.col_data = CollectionOperation(self.nickname)
        self.pre_crawl_time = time.time()

    def get_all_reading_data(self, filter=None, process=None):
        """
        :param filter:
        :return: 轮流调用wx_req_data_list中的微信参数 采集文章的阅读数据
        """
        if 'getappmsgext' in self.wx_req_data_list[0]:
            raw_articles = self.col_data.get(read_num={'$exists': False})
            cnt = 0
            for a in raw_articles:
                if 'mp.weixin.qq.com' in a['content_url']:
                    if 'comment_id' not in a:
                        a['comment_id'] = 0
                    self.articles.append([cnt, a['content_url'], a['comment_id']])
                    cnt += 1

            for itme in self.articles:
                while time.time() - self.pre_crawl_time <= self.delay:
                    time.sleep(0.05)

                self.pre_crawl_time = time.time()
                reading_data = Crawler(itme[1], itme[2], self.wx_req_data_list[itme[0] % self.wx_num]).run()
                reading_data = self.check(reading_data, itme)
                reading_data['id'] = get_md5(itme[1])
                self.col_data.insert('id', reading_data)
                process.new_reading_data(itme[0] + 1, len(self.articles), self.delay)

        else:
            logger.warning('点击查看该公众号的任意一篇文章且出现阅读量')

    def save(self, reading_data):
        """
        :param reading_data:
        :return: 保存数据
        """
        pass

    def prepare_task(self):
        """
        :return: 多线程的方式准备任务
        """
        for item in self.articles:
            yield {'index':item[0], 
             'url':item[1]}

    def task_handler(self, task):
        """
        :return: 多线程的方式任务处理器
        """
        Crawler(task['url'], self.wx_req_data_list[task['index'] % self.wx_num]).run()

    def check(self, reading_data, item):
        """
        :return: 带着本次请求的参数和结果一起过安检
        请求失败导致安检不通过 安检提醒人重新操作手机 操作完之后再次发起请求
        不排除还是会失败  继续调用自己 反正想办法让其获得成功的请求  最后返回成功的请求
        """
        if reading_data != 'req_data_error':
            stop_and_start.check({'crawler':'阅读数据',  'msg':'success'})
        else:
            stop_and_start.check({'crawler':'阅读数据',  'msg':'req_data_error'})
            self.wx_req_data_list = rd.tidy()
            while len(self.wx_req_data_list) == 0:
                self.wx_req_data_list = rd.tidy()
                from utils.front import notification
                notification('没有发现参数', '参数错误', _type='error')
                time.sleep(3)

            reading_data = Crawler(item[1], item[2], self.wx_req_data_list[0]).run()
            self.check(reading_data, item)
        return reading_data