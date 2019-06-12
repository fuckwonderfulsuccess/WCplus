# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\search.py
"""
为搜索相关的界面提供数据
"""

def l11l11lll_wcplus_():
    """
    根据index的数据 提供搜索选项
    1. 可用的搜索范围
    2. index的总文档数
    """
    from app.search.search import l1ll111l1_wcplus_
    index_list = l1ll111l1_wcplus_.l1l1l1ll1_wcplus_()
    l11l1l11l_wcplus_ = 0
    l11l1l111_wcplus_ = []
    for i in index_list:
        l11l1l11l_wcplus_ += i[1]
        l11l1l111_wcplus_.append({'value':i[0],  'lable':'%s %d' % (i[0], i[1])})

    l11l1l111_wcplus_ = [
     {'value':'全部', 
      'lable':'全部 ' + str(l11l1l11l_wcplus_)}] + l11l1l111_wcplus_
    return l11l1l111_wcplus_


if __name__ == '__main__':
    print(l11l11lll_wcplus_())