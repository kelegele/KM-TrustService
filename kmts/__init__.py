from mcdreforged.plugin.si.plugin_server_interface import PluginServerInterface
from mcdreforged.info_reactor.info import Info
import re
from .constants import VERSION
from .utils.misc.context import Context
from .utils.command import initCommandSystem
from .shared import gctx

from .utils.configUtils import readFile, writeFile
from mcdreforged.api.decorator.new_thread import new_thread
import time


def on_load(server: PluginServerInterface, _):
    server.logger.info(f'KMTS MCDR Plugin loaded: Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]}')
    server.logger.info("KMTS Copyright (c) wangyupu 2025. Publish under MIT License")

    initCommandSystem(server)

    readFile()
    server.logger.info(
        f"Success load permission file with {len(gctx.playerLevelsConfigFileContent['players'])} players.")


def on_unload(server: PluginServerInterface):
    gctx.saveLock.acquire()
    writeFile()
    gctx.saveLock.release()


@new_thread()
def autoSave():  # 自动保存
    serverLogger = PluginServerInterface.get_instance().logger
    while not gctx.firstOP:  # 进行一次保存
        time.sleep(10)
    writeFile()
    serverLogger.info("首次保存权限文件完成")
    while True:
        time.sleep(60*30)
        if gctx.saveLock.acquire_lock(blocking=False):
            writeFile()
            serverLogger.info("自动保存权限文件完成")
            gctx.saveLock.release()
        else:  # 无法获得锁说明在退出过程
            break
