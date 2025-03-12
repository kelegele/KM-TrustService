#
from mcdreforged.api.command import SimpleCommandBuilder, Text, Integer
from mcdreforged.command.command_source import CommandSource
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.minecraft.rtext.text import RText
from mcdreforged.minecraft.rtext.style import RColor

from .classes import upgradeRequest

from ...shared import gctx
from ..permissionUtils.point import getUpgradeCost, getUpgradeAddInt, canUpgrade, getPointName
from ..configUtils import readPlayerInfo, Player


def printHelp(source: CommandSource, context: CommandContext):
    # 准备帮助信息
    nextLine = RText("\n")

    title = RText("< ", RColor.dark_purple) + RText("KeleMC", RColor.yellow) + \
        RText(" 玩家信任服务 帮助") + RText(" >", RColor.dark_purple)
    body = RText('''\
!!ts: 输出本条消息
!!ts upgrade <玩家名称>: 升级某个玩家，同时消耗你的信任点数''')

    if not source.is_console:
        try:
            player = readPlayerInfo(source.player)
        except:
            player = Player(source.player, False, 0)
    else:
        player = Player("<Console>", True, 999)
    body2 = RText("< ") + RText("您的信息 ", RColor.dark_purple) + RText(" >") + RText(f'''
名称: {source.player}
等级: {getPointName(player)}
剩余信任点: {player.trustPoint}
可用命令列表:
''')

    final = title + nextLine + body + nextLine + body2
    source.reply(final)


def upgradePlayer(source: CommandSource, context: CommandContext):
    playerStorageName = None
    if source.is_console:
        playerStorageName = "<Console>"
    else:
        playerStorageName = source.player

    alreadyExistRequest = gctx.playerUpgradeAwaits.get(playerStorageName, None)

    if alreadyExistRequest:
        source.reply(RText(f"您已经请求升级 {alreadyExistRequest.targetPlayer}，但是您又运行了这个命令，所以上个请求将被忽略。", RColor.green))

    if source.is_player:
        if source.player == context['playerName']:
            source.reply(RText("您不能升级自己！", RColor.red))
            try:
                del gctx.playerUpgradeAwaits[playerStorageName]
            except KeyError:
                pass
            finally:
                return

        try:
            player = readPlayerInfo(source.player)
        except KeyError:
            source.reply(RText("您为1级玩家，无法升级！", RColor.red))
            return
        if not canUpgrade(player):
            source.reply(RText("您的信任点不足，无法升级！", RColor.red))
            return

        req = upgradeRequest(playerStorageName, context['playerName'], getUpgradeCost(player), getUpgradeAddInt(player))
        source.reply(f"您将花费{req.cost}信任点以为 {context['playerName']} 增加{req.add}信任点。确认请输入`!!ts confirm`")
        gctx.playerUpgradeAwaits[playerStorageName] = req
    elif source.is_console:
        source.reply(f"以控制台执行的upgrade子命令将以根玩家的权限执行(为目标增加17点数)。确认请输入`!!ts confirm`")


def playerUpgradeConfirm(source: CommandSource, context: CommandContext):
    playerStorageName = None
    if source.is_console:
        playerStorageName = "<Console>"
    else:
        playerStorageName = source.player

    alreadyExistRequest: upgradeRequest = gctx.playerUpgradeAwaits.get(playerStorageName, None)

    if not alreadyExistRequest:
        source.reply(RText("您还没有发出升级请求！", RColor.red))
    else:
        try:
            del gctx.playerUpgradeAwaits[playerStorageName]
        except KeyError:
            pass

        source.reply(RText(
            f"正在为玩家 {alreadyExistRequest.targetPlayer} 升级，您减少了 {alreadyExistRequest.cost} 信任点，对方增加了 {alreadyExistRequest.add} 信任点。", RColor.green))


def playerPointSet(source: CommandSource, context: CommandContext):
    if not source.has_permission_higher_than(3):
        source.reply(RText("你没有权限执行这个操作！", RColor.red))


def getTSCmdBuilder():
    cmdBuilder = SimpleCommandBuilder()

    cmdBuilder.command("!!ts", printHelp)
    cmdBuilder.command("!!ts upgrade <playerName>", upgradePlayer)
    cmdBuilder.command("!!ts confirm", playerUpgradeConfirm)

    cmdBuilder.command("!!ts setPoint <playerName> <point>", playerPointSet)

    cmdBuilder.arg('playerName', Text)
    cmdBuilder.arg('point', Integer)

    return cmdBuilder


def initCommandSystem(serverInstance):
    getTSCmdBuilder().register(serverInstance)
    serverInstance.register_help_message("!!ts", "KeleMC 玩家信任服务")
    serverInstance.register_help_message("!!ts upgrade", "消耗自身点数升级某人")
    serverInstance.register_help_message("!!ts setPoint", "设置某人权限", 4)

    serverInstance.logger.info("成功注册命令")
