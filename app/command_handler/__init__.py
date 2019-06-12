# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\command_handler\__init__.py
"""
一个命令对应该模块下的一份python文件
注册时指定命令和处理模块
"""
from app.command_handler.l111ll1ll_wcplus_ import l111ll1l1_wcplus_
commands = {'index all gzh': l111ll1l1_wcplus_()}

def execute_command(command):
    """
    :param command:
    :return: 参数使用 ' - ' 间隔
    """
    from utils.front import l1l11111l_wcplus_
    cmd = command.split(' - ')[0]
    l111llll1_wcplus_ = command.split(' - ')[1:]
    if cmd not in commands:
        l1l11111l_wcplus_(command, '不支持的命令', _type='error')
    else:
        l1l11111l_wcplus_(command, '开始执行', _type='success')
        from threading import Thread
        (Thread(target=commands[cmd].run, args=(cmd, l111llll1_wcplus_))).start()