# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Mar 29 2019, 00:03:27) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\delete.py
"""
负责删除工作
"""

class DeleteGZH:
    """
    删除一个公众号的全部数据
    """

    def __init__(self, nickname):
        self.nickname = nickname

    def l11llll1l_wcplus_(self):
        from cmp.db.l1ll11l11_wcplus_ import l11llllll_wcplus_
        l11llllll_wcplus_.drop_collection(self.nickname)

    def l11lllll1_wcplus_(self):
        from instance import l1l1l11l1_wcplus_
        l1l1l11l1_wcplus_.delete(nickname=self.nickname)

    def l1l111111_wcplus_(self):
        """
        :return: wcplus的设计初衷是希望大家尽可能多保存微信数据
        暂时设定手动删除html文档
        """
        pass

    def l1l1lll11_wcplus_(self):
        """
        :return: 从索引中删除
        """
        from app.search.index import l1l1lll1l_wcplus_
        l1l1lll1l_wcplus_(self.nickname).delete()

    def run(self):
        try:
            self.l11llll1l_wcplus_()
            self.l11lllll1_wcplus_()
            self.l1l111111_wcplus_()
            self.l1l1lll11_wcplus_()
        except:
            from utils.base import logger
            logger.warning('删除数据遇到一个警告')

        from utils.front import l1l11111l_wcplus_
        l1l11111l_wcplus_(self.nickname, '删除完成 刷新页面公众号消失', 'success')