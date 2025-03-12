from dataclasses import dataclass, Field


@dataclass
class Player:
    playerName: str
    isRootPlayer: bool
    trustPoint: int
