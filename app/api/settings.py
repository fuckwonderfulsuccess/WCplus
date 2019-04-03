# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: app\api\settings.py
"""
提供数据设置API
"""
from cmp.db.mongo import CollectionOperation
col_settings = CollectionOperation('settings')

class Settings:

    def __int__(self):
        pass

    def get(self):
        """
        :return: 获取所有的设置字段{}
        """
        sd = col_settings.get()
        settings_data = {}
        for s in sd:
            settings_data[s['key']] = s['value']

        from cmp.protect import Passport, get_uuind
        settings_data['uuid'] = Passport.get_mac_address()
        passport = Passport.check_password()
        if not passport:
            settings_data['passport'] = 0
        else:
            settings_data['passport'] = passport
        settings_data['proxy_server'] = get_uuind()[-1]
        return settings_data

    def insert(self, settings_data_dict):
        """
        :param settings_data_dict: settings数据本质上是一个字典
        :return: 插入或修改
        """
        settings_data_list = []
        for key in settings_data_dict:
            item = {}
            item['key'] = key
            item['value'] = settings_data_dict[key]
            settings_data_list.append(item)

        col_settings.insert('key', settings_data_list)

    def delete(self, key, all=False):
        """
        :param key:准确的key
        :param all:
        :return:
        """
        if all:
            col_settings.delete()
        else:
            col_settings.delete(key=key)