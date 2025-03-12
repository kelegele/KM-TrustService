#

class Context:
    def __init__(self):
        self.playerUpgradeAwaits = dict()
        self.playerOnline = set()
        self.playerOnlineUpdated = False
