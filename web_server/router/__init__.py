# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: web_server\router\__init__.py
"""
页面路由
"""
from web_server import web_app
from flask import render_template, send_from_directory

@web_app.route('/', methods=['GET'])
def index():
    """
    :return: 返回首页
    """
    return render_template('index.html')


@web_app.route('/img/<filename>', methods=['GET'])
def get_img(filename):
    """
    :param filename:
    :return: 返回一个静动态文件
    """
    print(filename)
    return send_from_directory(directory='web_server/static/img/', filename=filename)


@web_app.route('/html/<nickname>/<md5>', methods=['GET'])
def get_html_doc(nickname, md5):
    """
    :param filename:
    :return: 返回一个静动态文件
    """
    from cmp.db.mongo import CollectionOperation
    if CollectionOperation(nickname).count(id=md5, comment_id={'$exists': True}):
        from webbrowser import open
        import os
        file_name = os.getcwd() + '/web_server/static/html/' + nickname + '/' + md5 + '.html'
        open(file_name)
        return ('', 204)
    return '未保存该文章 请先采集'