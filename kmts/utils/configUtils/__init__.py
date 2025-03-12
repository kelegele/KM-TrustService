from mcdreforged.plugin.si.server_interface import ServerInterface
from mcdreforged.plugin.si.plugin_server_interface import PluginServerInterface
from ...shared import gctx
from .classes import Player

defaultPermissionFile = {
    'rootPlayers': [],
    'players': {}
}


def readPlayerInfo(playerName) -> Player:
    # 读取基本信息
    try:
        rawInfo = gctx.playerLevelsConfigFileContent['players'][playerName]
    except KeyError:
        raise KeyError("不存在的玩家")

    isRoot = False
    if rawInfo['name'] in gctx.playerLevelsConfigFileContent['rootPlayers']:
        isRoot = True

    return Player(rawInfo['name'], isRoot, rawInfo['points'])


def savePlayerInfo(playerInfo: Player) -> None:
    gctx.playerLevelsConfigFileContent['players'][playerInfo.playerName] = {
        "name": playerInfo.playerName,
        "points": playerInfo.trustPoint,
    }


def readFile():  # 插件加载时调用
    PSI: PluginServerInterface = ServerInterface.psi()
    cfg = PSI.load_config_simple("permission.json", defaultPermissionFile)
    gctx.playerLevelsConfigFileContent = cfg


def writeFile():  # 插件卸载时调用
    PSI: PluginServerInterface = ServerInterface.psi()
    PSI.save_config_simple(gctx.playerLevelsConfigFileContent, "permission.json")
