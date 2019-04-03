# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\db\sqlite\data_schema.py
from peewee import SqliteDatabase
from config import SQLITE_DB_NAME
sqlite_db = SqliteDatabase(SQLITE_DB_NAME)
sqlite_db.connect()
from peewee import Model
from peewee import CharField, IntegerField, TextField, DateTimeField
from datetime import datetime

class Data(Model):
    id = CharField(default='')
    nickname = CharField(default='')
    title = CharField(default='')
    article_id = IntegerField(default=-2)
    content_url = CharField(default='')
    source_url = CharField(default='')
    digest = TextField(default='')
    machine_digest = TextField(default='')
    cover = CharField(default='')
    p_date = DateTimeField(default=datetime(2000, 1, 1))
    with_ad = IntegerField(default=-2)
    pic_num = IntegerField(default=-2)
    video_num = IntegerField(default=-2)
    read_num = IntegerField(default=-2)
    like_num = IntegerField(default=-2)
    comment_id = CharField(default='')
    comment_num = IntegerField(default=-2)
    comments = TextField(default='{}')
    reward_num = IntegerField(default=-2)
    author = CharField(default='')
    copyright_stat = CharField(default='')
    mov = IntegerField(default=-2)
    title_emotion = IntegerField(default=-2)
    title_token = TextField(default='[]')
    title_token_len = IntegerField(default=-2)
    human_digest_token = TextField(default='[]')
    article = TextField(default='')
    html = TextField(default='')
    article_token = TextField(default='[]')
    article_token_len = IntegerField(default=-2)
    c_date = DateTimeField(default=datetime(2000, 1, 1))

    class Meta:
        database = sqlite_db


class ReqData(Model):
    id = CharField(default='')
    time = DateTimeField(default=datetime.now())
    key = CharField(default='')
    value = TextField(default='')

    class Meta:
        database = sqlite_db


class CrawlerLog(Model):
    id = CharField(default='')
    nickname = CharField(default='')
    num = TextField(default='')
    time = DateTimeField(default=datetime.now())

    class Meta:
        database = sqlite_db


sqlite_db.create_tables([Data, ReqData, CrawlerLog])