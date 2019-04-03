# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: cmp\proxy_server\__init__.py
"""
代理服务器模块
"""
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from cmp.proxy_server.addons import SelfAddon

def start_proxy():
    self_addon = SelfAddon()
    opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(self_addon)
    try:
        m.run()
    except KeyboardInterrupt:
        print('')
        m.shutdown()


if __name__ == '__main__':
    start_proxy()