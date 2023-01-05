from abc import ABC, abstractmethod
from typing import Optional

from wizard.card import Card
from wizard.color import Color, TrumpColor


class Player(ABC):
    def __init__(self, name: str):
        self.cards: list[Card] = []
        self.name = name

    @abstractmethod
    def bid_tricks(self, allowed_bids: list[int]) -> int:
        """
        Bid the number of tricks the player will get in the round.
        :param allowed_bids: The allowed bids
        :return: The forecasted number of tricks
        """

    @abstractmethod
    def choose_trump_color(self) -> TrumpColor:
        """
        Choose the trump color based on the player's cards
        :return: the trump color. Notice that NO_TRUMP is not allowed as a return value!
        """

    @abstractmethod
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
        """
        Decide which card to play next. This is where the magic happens.
        :param played_cards: The cards already played in the trick. The order corresponds to the order of the players
        :param currently_highest: The currently highest card in the round, if it exists.
        :param following_suit: The current suit to follow, if it exist
        :param trump_color: The trump color
        :param cards_players: The dictionary indicating the player for each played card.
        :param players: The players of the trick, where the ordering is as the game specifies it
        :param bidden_tricks: For each player the number of tricks bidden in the current round.
        :param taken_tricks: For each player the number of tricks already taken in the current round.
        :return: The card to play.
        """
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
