#
from ..configUtils.classes import Player
from ...shared import gctx


def getUpgradeCost(player, addPoint: int) -> int:
    if player.isRootPlayer:
        return 0
    costPoint = max(int(addPoint*gctx.configFileContent['trustPointConfig']['upgrades']['cost']['mul']) +
                    addPoint, addPoint+gctx.configFileContent['trustPointConfig']['upgrades']['cost']['min'])
    return costPoint


def getUpgradeLevel(player: Player, costPoint: int) -> int:
    UpgradedtrustPoint = player.trustPoint - costPoint
    if player.isRootPlayer:
        return "根玩家"
    elif UpgradedtrustPoint == 0:
        return "1级玩家"
    else:
        p = UpgradedtrustPoint
        match p:
            case p if gctx.configFileContent['trustPointConfig']['levels']['2']['begin'] <= p < gctx.configFileContent['trustPointConfig']['levels']['2']['end']:
                return "2级玩家"
            case p if gctx.configFileContent['trustPointConfig']['levels']['3']['begin'] <= p < gctx.configFileContent['trustPointConfig']['levels']['3']['end']:
                return "3级玩家"
            case p if p > gctx.configFileContent['trustPointConfig']['max']:
                return "管理员或根玩家"


def canUpgrade(player: Player, costPoint: int):
    if (player.isRootPlayer):
        return True
    if player.trustPoint - costPoint < 0:
        return False
    return True


def getPointName(player: Player) -> str:
    if player.isRootPlayer:
        return "根玩家"
    elif player.trustPoint == 0:
        return "1级玩家"
    else:
        p = player.trustPoint
        match p:
            case p if gctx.configFileContent['trustPointConfig']['levels']['2']['begin'] <= p < gctx.configFileContent['trustPointConfig']['levels']['2']['end']:
                return "2级玩家"
            case p if gctx.configFileContent['trustPointConfig']['levels']['3']['begin'] <= p <= gctx.configFileContent['trustPointConfig']['levels']['3']['end']:
                return "3级玩家"
            case p if p > gctx.configFileContent['trustPointConfig']['max']:
                return "管理员或根玩家"


def getMCDRPermissionLevel(player: Player) -> int | None:
    if player.isRootPlayer:
        return None
    elif player.trustPoint == 0:
        return 0
    else:
        p = player.trustPoint
        match p:
            case p if gctx.configFileContent['trustPointConfig']['levels']['2']['begin'] <= p < gctx.configFileContent['trustPointConfig']['levels']['2']['end']:
                return 1
            case p if gctx.configFileContent['trustPointConfig']['levels']['3']['begin'] <= p <= gctx.configFileContent['trustPointConfig']['levels']['3']['end']:
                return 2
            case p if p > gctx.configFileContent['trustPointConfig']['max']:
                return None


def isUpgradeUseless(player1: Player, addPoint: int) -> bool:
    if player1.isRootPlayer:
        return True
    elif player1.trustPoint + addPoint > gctx.configFileContent['trustPointConfig']['max']:
        return True
    return False
