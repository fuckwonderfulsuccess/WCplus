# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.6 (default, Jan 26 2019, 16:53:05) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Embedded file name: web_server\event\__init__.py
"""
websocket事件监听
"""
from web_server import socketio

@socketio.on('connect')
def handle_message_connected():
    socketio.emit('connect', {'data': 'hand shake'})


@socketio.on('hello')
def handle_hello(data):
    print(data)


@socketio.on('pause')
def handle_pause(data):
    from instance import stop_and_start
    if data:
        stop_and_start.stop()
    else:
        stop_and_start.start()


@socketio.on('ask_data')
def handle_ask_data(data):
    if data == 'req_data':
        from app.api.crawler import ReqData
        ReqData().send()
    try:
        import builtins
        builtins.crawler_process.send_process()
    except:
        pass


@socketio.on('export_excel')
def handle_export_excel(nickname):
    nickname = (nickname.encode(encoding='raw_unicode_escape')).decode('utf-8')
    from app.export.excel import ExportExcel
    ExportExcel(nickname).run()


@socketio.on('delete_gzh')
def handle_delete_gzh(nickname):
    nickname = (nickname.encode(encoding='raw_unicode_escape')).decode('utf-8')
    from app.api.delete import DeleteGZH
    DeleteGZH(nickname).run()