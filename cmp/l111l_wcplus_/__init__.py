# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\l111l_wcplus_\__init__.py
"""
代理服务器模块
"""
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from cmp.l111l_wcplus_.addons import l1lll111l1l_wcplus_

def l11ll_wcplus_():
    l1ll1llll11_wcplus_ = l1lll111l1l_wcplus_()
    opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
    l1ll1lll1ll_wcplus_ = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(l1ll1lll1ll_wcplus_)
    m.addons.add(l1ll1llll11_wcplus_)
    try:
        m.run()
    except KeyboardInterrupt:
        print('')
        m.shutdown()


if __name__ == '__main__':
    l11ll_wcplus_()