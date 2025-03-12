from mcdreforged.plugin.si.plugin_server_interface import PluginServerInterface
from mcdreforged.info_reactor.info import Info
import re
from .constants import VERSION
from .utils.misc.context import Context
from .utils.command import initCommandSystem
from .shared import gctx

from .utils.configUtils import readFile, writeFile


def on_load(server: PluginServerInterface, _):
    server.logger.info(f'KMTS MCDR Plugin loaded: Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]}')
    server.logger.info("KMTS Copyright (c) wangyupu 2025. Publish under MIT License")

    initCommandSystem(server)

    readFile()


def on_unload(server: PluginServerInterface):
    writeFile()
