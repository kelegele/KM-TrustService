#
from ..configUtils.classes import Player


def getUpgradeCost(player: Player) -> int:
    if player.isRootPlayer:
        return 0
    elif player.trustPoint == 0:
        return False
    else:
        p = player.trustPoint
        match p:
            case p if 1 <= p < 13:
                return 5
            case p if 14 <= p <= 27:
                return 8
            case p if p > 27:
                return 0


def getUpgradeAddInt(player: Player) -> int:
    if player.isRootPlayer:
        return 16
    elif player.trustPoint == 0:
        return False
    else:
        p = player.trustPoint
        match p:
            case p if 1 <= p < 13:
                return 4
            case p if 14 <= p <= 27:
                return 7
            case p if p > 27:
                return 8


def canUpgrade(player: Player):
    if not getUpgradeCost(player):
        return False
    if player.trustPoint - getUpgradeCost(player) < 0:
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
            case p if 1 <= p < 13:
                return "2级玩家"
            case p if 14 <= p <= 27:
                return "3级玩家"
            case p if p > 27:
                return "管理员或根玩家"


def getMCDRPermissionLevel(player: Player) -> int:
    if player.isRootPlayer:
        return None
    elif player.trustPoint == 0:
        return 0
    else:
        p = player.trustPoint
        match p:
            case p if 1 <= p < 13:
                return 1
            case p if 14 <= p <= 27:
                return 2
            case p if p > 27:
                return None
