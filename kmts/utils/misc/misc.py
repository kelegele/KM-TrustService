from mcdreforged.plugin.si.server_interface import ServerInterface
from ...shared import gctx


def getOnlinePlayers():  # 刷新ctx里的集合同时返回那个集合
    server = ServerInterface.get_instance()
    server.execute("list")  # 这个不返回命令结果，需要单独监听，事件监听代码见__init__.py
    server.logger.info("Command was executed.")
    # 等待更新
    while not gctx.playerOnlineUpdated:
        pass
    gctx.playerOnlineUpdated = False
    return gctx.playerOnline
