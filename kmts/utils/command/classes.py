from dataclasses import dataclass


@dataclass
class upgradeRequest:
    requestPlayer: str
    targetPlayer: str
    cost: int
