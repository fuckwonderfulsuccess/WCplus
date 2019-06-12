# Python bytecode 3.6 (3372)
# Embedded file name: main.py
# Decompiled by https://python-decompiler.com
"""

"""
from threading import Thread
from multiprocessing import Process
import multiprocessing
from l1l11_wcplus_ import l1ll1l_wcplus_
from cmp.l111l_wcplus_ import l11ll_wcplus_
import webbrowser, time

def l111l_wcplus_():
    """
    :return:
    """
    l11ll_wcplus_()


def l1llll_wcplus_():
    """
    :return: 
    """
    from app.api.l1lll1_wcplus_ import l1111_wcplus_
    while True:
        l1111_wcplus_().send()
        time.sleep(3)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    Process(target=l111l_wcplus_).start()
    Thread(target=l1llll_wcplus_).start()
    webbrowser.open('http://localhost:5000')
    l1ll1l_wcplus_()
