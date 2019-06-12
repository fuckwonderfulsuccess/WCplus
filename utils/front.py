# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\front.py
"""
前端相关的一些方法 不能单独在web中使用需要web服务和相关前端代码的配合
"""

def message(message, _type=''):
    """
    :param _type: 默认 success warning error
    :param message:
    :return: 顶部下拉消息
    """
    from l1l11_wcplus_ import socketio
    socketio.emit('message', {'type':_type,  'message':message})


def l1l111lll_wcplus_(message, title, _type=''):
    """
    :param message:默认 success warning error
    :param title:
    :param _type:
    :return: 弹窗消息
    """
    from l1l11_wcplus_ import socketio
    socketio.emit('message_box', {'message':message,  'title':title,  'type':_type})


def l1l11111l_wcplus_(message, title, _type='', duration=3):
    """
    :param message:默认 success warning error
    :param title:
    :param _type:
    :param duration: 消息显示时间 0表示消息不会自动关闭
    :return: 右侧消息
    """
    from l1l11_wcplus_ import socketio
    socketio.emit('notification', {'message':message,  'title':title,  'type':_type,  'duration':duration})


def l111lll11_wcplus_(item):
    """
    :param item:
    :return: 发送一条日志
    """
    from l1l11_wcplus_ import socketio
    socketio.emit('command', item)