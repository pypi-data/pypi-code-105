
from datetime import datetime
from typing import Dict
from pydantic import BaseModel

from .coin import Coin


class Wallet(BaseModel):
    exchange: str
    coins: Dict[str, Coin]
    sign: int
    time: float
    date: datetime

    def __getitem__(self, standard_name: str):
        if standard_name in self.coins:
            return self.sign * self.coins[standard_name]
        else:
            coin = Coin(name=standard_name, amount=0.0)
            self.coins[standard_name] = coin
            return self.sign * self.coins[standard_name]

    def __eq__(self, other):
        for coin in self.coins.values():
            other_coin = other[coin.name]
            if other_coin != coin:
                return False

        for other_coin in other.coins.values():
            our_coin = self[other_coin.name]
            if other_coin != our_coin:
                return False
        return True

    def __str__(self):
        out = ""
        for coin in self.coins.values():
            out += f"\t\t **{coin.name}**: {coin.amount}"
        return out
