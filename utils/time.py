# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: utils\time.py


def get_internet_time():
    """
    :return: 获取百度服务器时间
    """
    import requests, time, datetime
    try:
        r = requests.get(url='http://www.baidu.com')
        date = r.headers['Date']
        net_time = time.mktime(datetime.datetime.strptime(date[5:25], '%d %b %Y %H:%M:%S').timetuple()) + 28800
        return int(net_time)
    except:
        return


if __name__ == '__main__':
    net_time = get_internet_time()
    if net_time:
        print(net_time)