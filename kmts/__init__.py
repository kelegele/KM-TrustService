from mcdreforged.plugin.si.plugin_server_interface import PluginServerInterface
from mcdreforged.info_reactor.info import Info
import re
from .constants import VERSION
from .utils.misc.context import Context
from .utils.command import initCommandSystem
from .shared import gctx


def on_load(server: PluginServerInterface, _):
    server.logger.info(f'KMTS MCDR Plugin loaded: Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]}')
    server.logger.info("KMTS Copyright (c) wangyupu 2025. Publish under MIT License")

    initCommandSystem(server)


def on_info(server, info: Info):
    if not info.is_player and "There are" in info.content and "<" not in info.content:
        rePattern = r"There are \d+ of a max of \d+ players online: ([\w]+), ([\w]+), ([\w]+)"
        match = re.match(rePattern, info.content.strip())
        server.logger.info("List command result was matchd.")
        if match:
            data_items = match.group(1).split(', ')
            if not data_items[0]:
                gctx.playerOnline.clear()

            # 将提取的数据放入集合中
            gctx.playerOnline = set(data_items)
            gctx.playerOnlineUpdated = True
            return
        else:
            return
