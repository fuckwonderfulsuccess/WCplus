# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\export\excel.py
from cmp.db.mongo import CollectionOperation
import pandas as pd, os
from config import EXCEL_OUTPUT_FOLDER

class ExportExcel:

    def __init__(self, nickname):
        self.nickname = nickname
        if not os.path.exists(EXCEL_OUTPUT_FOLDER):
            os.makedirs(EXCEL_OUTPUT_FOLDER)

    def prepare_data(self):
        data_gen = CollectionOperation(self.nickname).get()
        return data_gen

    def create_dataframe(self, data_gen):
        df = pd.DataFrame(columns=['编号', '阅读', '点赞', '赞赏', '评论', '位置', '发文时间', '作者', '标题', '链接', '原文链接'])
        cnt = 0
        for a in data_gen:
            cnt += 1
            if 'read_num' not in a:
                a['read_num'] = '-'
            if 'like_num' not in a:
                a['like_num'] = '-'
            if 'reward_num' not in a:
                a['reward_num'] = '-'
            if 'comment_num' not in a:
                a['comment_num'] = '-'
            df.loc[cnt] = [cnt,
             a['read_num'],
             a['like_num'],
             a['reward_num'],
             a['comment_num'],
             a['mov'],
             a['p_date'],
             a['author'],
             a['title'],
             a['content_url'],
             a['source_url']]

        return df

    def create_excel(self, df):
        writer = pd.ExcelWriter(EXCEL_OUTPUT_FOLDER + self.nickname + '.xlsx')
        df.to_excel(writer, self.nickname)
        writer.save()

    def run(self):
        from utils.front import notification
        data_gen = self.prepare_data()
        df = self.create_dataframe(data_gen)
        self.create_excel(df)
        notification(self.nickname, '导出Excel完成', 'success')
        import subprocess
        from instance import PLATFORM
        if PLATFORM == 'osx':
            subprocess.call(['open', EXCEL_OUTPUT_FOLDER])
        else:
            if PLATFORM == 'win':
                subprocess.call(['explorer', EXCEL_OUTPUT_FOLDER.replace('/', '\\')])