# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\time.py


def l1lll1l11ll_wcplus_():
    """
    :return: 获取百度服务器时间
    """
    import requests, time, datetime
    try:
        r = requests.get(url='http://www.baidu.com')
        date = r.headers['Date']
        l1lll1ll111_wcplus_ = time.mktime(datetime.datetime.strptime(date[5:25], '%d %b %Y %H:%M:%S').timetuple()) + 28800
        return int(l1lll1ll111_wcplus_)
    except:
        from instance import l1_wcplus_
        if l1_wcplus_ == 'win':
            return
        import time
        return time.time()


if __name__ == '__main__':
    l1lll1ll111_wcplus_ = l1lll1l11ll_wcplus_()
    if l1lll1ll111_wcplus_:
        print(l1lll1ll111_wcplus_)