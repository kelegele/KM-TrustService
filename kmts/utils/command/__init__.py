#
from mcdreforged.api.command import SimpleCommandBuilder, Text, Integer
from mcdreforged.command.command_source import CommandSource
from mcdreforged.command.builder.common import CommandContext
from mcdreforged.minecraft.rtext.text import RText
from mcdreforged.minecraft.rtext.style import RColor

from .classes import upgradeRequest

from ...shared import gctx
from ..permissionUtils.point import getUpgradeCost, getUpgradeAddInt, canUpgrade, getPointName, getUpgradeLevel
from ..permissionUtils import updateAllPermissions
from ..configUtils import readPlayerInfo, Player, savePlayerInfo
from ..configUtils import writeFile


def printHelp(source: CommandSource, context: CommandContext):
    # 准备帮助信息
    nextLine = RText("\n")

    title = RText("< ", RColor.dark_purple) + RText("KeleMC", RColor.yellow) + \
        RText(" 玩家信任服务 帮助") + RText(" >", RColor.dark_purple)
    body = RText('''\
!!ts: 输出本条消息
!!ts upgrade <玩家名称> <点数>: 升级某个玩家，同时消耗你的信任点数''')

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
当前MCDR权限级别: {source.get_server().get_instance().get_permission_level(source)}
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
        addPoint = context['point']
        costPoint=getUpgradeCost(addPoint)
        if not canUpgrade(player):
            source.reply(RText("您的信任点不足，无法升级！", RColor.red))
            return

        req = upgradeRequest(playerStorageName, context['playerName'], costPoint, addPoint)
        source.reply(f"您将花费{req.cost}信任点以为 {context['playerName']} 增加{req.add}信任点。为对方升级后您的等级为{getUpgradeLevel(player)}。确认请输入`!!ts confirm`")
        gctx.playerUpgradeAwaits[playerStorageName] = req
    elif source.is_console:
        source.reply(f"以控制台执行的upgrade子命令将以根玩家的权限执行(为目标增加{context['point']}点数)。确认请输入`!!ts confirm`")


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

        # 升级逻辑
        # 先获得两个玩家对象
        try:
            player2 = readPlayerInfo(alreadyExistRequest.targetPlayer)
        except:
            player2 = Player(alreadyExistRequest.targetPlayer, False, 0)

        try:
            player1 = readPlayerInfo(alreadyExistRequest.requestPlayer)
        except:
            source.reply(RText("升级失败", RColor.red))
            return

        # 检查玩家2
        if player2.isRootPlayer:
            source.reply(RText("不能给根玩家升级", RColor.red))
            return
        if gctx.upgrade.acquire(False)

          # 然后先扣钱
          player1.trustPoint -= alreadyExistRequest.cost
          savePlayerInfo(player1)

          # 然后给target增加
          player2.trustPoint = min(player2.trustPoint   +alreadyExistRequest.add, 27)
          savePlayerInfo(player2)
          gctx.upgrade.release()
        else:
          source.reply(RText("当前正在升级，请重试", RColor.red))
          
        source.reply(RText(f"升级成功，对方现有 {player2.trustPoint} 信任点。", RColor.green))
        source.get_server().tell(alreadyExistRequest.targetPlayer, RText(
            f"{alreadyExistRequest.requestPlayer} 花费了 {alreadyExistRequest.cost}点信任点 给您 {alreadyExistRequest.add} 信任点。", RColor.green))

        # 更新权限
        updateAllPermissions()


def playerUpgradeConfirmWrapper(v0, v1):  # 方便后面加守卫语句
    gctx.upgradeProcessing.acquire()
    playerUpgradeConfirm(v0, v1)
    gctx.upgradeProcessing.release()


def playerPointSet(source: CommandSource, context: CommandContext):
    if not source.has_permission_higher_than(3):
        source.reply(RText("你没有权限执行这个操作！", RColor.red))
        return
    player = Player(context['playerName'], False, context['point'])
    savePlayerInfo(player)
    source.reply(RText(f"成功将玩家 {context['playerName']} 的点数设置为 {context['point']}", RColor.red))

    updateAllPermissions()


def savePermissionFile(source: CommandSource, _):
    if not source.has_permission_higher_than(2):
        source.reply(RText("你没有权限执行这个操作！", RColor.red))
        return
    if gctx.saveLock.acquire(False):
        writeFile()
        gctx.saveLock.release()
        source.reply(RText("成功保存权限文件。", RColor.green))
    else:
        source.reply(RText("锁被占用了，可能正在进行自动保存。", RColor.red))


def getTSCmdBuilder():
    cmdBuilder = SimpleCommandBuilder()

    cmdBuilder.command("!!ts", printHelp)
    cmdBuilder.command("!!ts upgrade <playerName> <point>", upgradePlayer)
    cmdBuilder.command("!!ts confirm", playerUpgradeConfirmWrapper)
    cmdBuilder.command("!!ts save", savePermissionFile)

    cmdBuilder.command("!!ts setPoint <playerName> <point>", playerPointSet)

    cmdBuilder.arg('playerName', Text)
    cmdBuilder.arg('point', Integer)

    return cmdBuilder


def initCommandSystem(serverInstance):
    getTSCmdBuilder().register(serverInstance)
    serverInstance.register_help_message("!!ts", "KeleMC 玩家信任服务")
    serverInstance.register_help_message("!!ts upgrade", "消耗自身点数升级某人")

    serverInstance.logger.info("成功注册命令")
