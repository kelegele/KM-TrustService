#
from mcdreforged.plugin.si.server_interface import ServerInterface
from ...shared import gctx
from ..configUtils import readPlayerInfo
from ..permissionUtils.point import getMCDRPermissionLevel, getPointName
from mcdreforged.minecraft.rtext.text import RText
from mcdreforged.minecraft.rtext.style import RColor


def setPermissionLevelForPlayer(playerName, targetLevel):
    pass


def updateAllPermissions():
    server = ServerInterface.get_instance()

    for playerName, _ in gctx.playerLevelsConfigFileContent['players'].items():
        if server.get_permission_level(playerName) != getMCDRPermissionLevel(readPlayerInfo(playerName)):
            if server.get_permission_level(playerName) >= 3:
                continue
            # 更新玩家权限，同时广播告知
            server.tell(playerName, RText(f"你现在是")+RText(getPointName(readPlayerInfo(playerName)),
                        RColor.aqua)+RText(f"了！"))
            server.set_permission_level(playerName, getMCDRPermissionLevel(readPlayerInfo(playerName)))
