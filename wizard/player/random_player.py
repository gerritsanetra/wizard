from random import Random
from typing import Optional

from wizard.card import Card
from wizard.color import Color, TrumpColor
from wizard.player.player import Player


class RandomPlayer(Player):
    def __init__(self, seed: int, name: str):
        super().__init__(name)
        self.random = Random(seed)

    def bid_tricks(self, allowed_bids: list[int]) -> int:
        return self.random.choice(allowed_bids)

    def choose_trump_color(self) -> TrumpColor:
        color = TrumpColor.NO_TRUMP
        while color == TrumpColor.NO_TRUMP:
            color = self.random.choice(list(TrumpColor))
        return color

    def play_next_card(
            self,
            played_cards: list[Card],
            currently_highest: Optional[Card],
            following_suit: Optional[Color],
            trump_color: TrumpColor,
            cards_players: dict[Card, "Player"],
            players: list["Player"],
            bidden_tricks: dict["Player", int],
            taken_tricks: dict["Player", int]
    ) -> Card:
        playable_cards = [card for card in self.cards if card.is_playable(self.cards, following_suit)]
        if len(playable_cards) == 0:
            raise RuntimeError("Something went wrong!")
        return self.random.choice(playable_cards)
