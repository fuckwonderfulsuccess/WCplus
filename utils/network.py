# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\network.py


def l111lllll_wcplus_():
    """
    :return: 获取局域网IP地址
    """
    from instance import l1_wcplus_
    if l1_wcplus_ == 'win':
        import socket
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    if l1_wcplus_ == 'osx':
        return '终端运行 ifconfig 查看'


if __name__ == '__main__':
    print(l111lllll_wcplus_())