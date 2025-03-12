#
from mcdreforged.api.command import SimpleCommandBuilder, Text, Integer
from mcdreforged.command.command_source import CommandSource
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.minecraft.rtext.text import RText
from mcdreforged.minecraft.rtext.style import RColor

from .classes import upgradeRequest

from ...shared import gctx
from ..misc.misc import getOnlinePlayers


def printHelp(source: CommandSource, context: CommandContext):
    # 准备帮助信息
    nextLine = RText("\n")

    title = RText("< ", RColor.dark_purple) + RText("KeleMC", RColor.yellow) + \
        RText(" 玩家信任服务 帮助") + RText(" >", RColor.dark_purple)
    body = RText('''\
!!ts: 输出本条消息
!!ts upgrade <玩家名称>: 升级某个玩家，同时消耗你的信任点数''')

    body2 = RText("您的信息: ", RColor.dark_purple) + RText(f'''
名称: undefined
等级: undefined
剩余信任点: undefined
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

    print(getOnlinePlayers())
    if not context['playerName'] in getOnlinePlayers():
        source.reply(RText(f"您请求升级的 {context['playerName']} 不在线！", RColor.red))
        try:
            del gctx.playerUpgradeAwaits[playerStorageName]
        except KeyError:
            pass
        return

    if source.is_player:
        source.reply(f"您将花费undefined信任点以为undefined增加undefined信任点。确认请输入`!!ts confirm`")
        gctx.playerUpgradeAwaits[playerStorageName] = upgradeRequest(playerStorageName, context['playerName'], 1)
    elif source.is_console:
        source.reply("以控制台执行的upgrade子命令将以根玩家的权限执行(为目标增加...点数)。确认请输入`!!ts confirm`")


def playerUpgradeConfirm(source: CommandSource, context: CommandContext):
    pass


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
