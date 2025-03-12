#
from threading import Lock


class Context:
    def __init__(self):
        self.playerUpgradeAwaits = dict()
        self.playerLevelsConfigFileContent = dict()

        self.upgradeProcessing = Lock()
