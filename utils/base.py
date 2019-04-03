# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\base.py
from loguru import logger
import pprint
pp = pprint.PrettyPrinter(depth=3)
debug_p = pp.pprint

def validate_file_name(file_name):
    """
    :param file_name:等待验证的文件名
    :return: 验证windows文件名的合法性 将不合法的字符替换为 下划线_
    """
    import re
    rstr = '[\\/\\\\\\:\\*\\?\\"\\<\\>\\|\\“\\”]'
    new_file_name = re.sub(rstr, '_', file_name)
    return new_file_name


def the_platform():
    from sys import platform
    if platform == 'linux' or platform == 'linux2':
        return 'linux'
    if platform == 'darwin':
        return 'osx'
    if platform == 'win32':
        return 'win'