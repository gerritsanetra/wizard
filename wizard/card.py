from abc import ABC, abstractmethod
from typing import Optional, Collection

from wizard.color import Color, TrumpColor
from wizard.constants import MIN_NUMBER, MAX_NUMBER, NUM_JESTERS, NUM_WIZARDS


class Card(ABC):
    @abstractmethod
    def is_highest(self, 
                   currently_highest: Optional["Card"], 
                   following_suit: Optional[Color],
                   trump_color: TrumpColor) -> bool:
        """
        Indicates, if the card is higher than the previous cards.
        The previous cards are sorted by the order of the current round.
        :param currently_highest: The currently highest card in the round, if it exists.
        :param following_suit: The current suit to follow, if it exist
        :param trump_color: The trump color
        :return: If the card is higher than all others
        """

    @abstractmethod
    def is_playable(self, player_cards: Collection["Card"], following_suit: Optional[Color]) -> bool:
        """
        Indicates, if the card can be played given the cards the player has and the following suit in the game.
        :param player_cards: all cards available to the player
        :param following_suit: The current suit to follow, if it exist
        :return: If the card can be played.
        """


class ColoredCard(Card):
    def __init__(self, number: int, color: Color) -> None:
        if not (MIN_NUMBER <= number <= MAX_NUMBER):
            raise ValueError(f"The number {number} is not feasible for a colored card!")
        self.number = number
        self.color = color

    def is_highest(self, currently_highest: Optional["Card"],
                   following_suit: Optional[Color], trump_color: TrumpColor) -> bool:
        if currently_highest is None:
            return True
        if isinstance(currently_highest, Wizard):
            return False
        elif isinstance(currently_highest, Jester):
            return True
        elif isinstance(currently_highest, ColoredCard):
            # the currently highest card is a colored card implies that a suit needs to be followed
            following_suit: Color
            if self.is_trump(trump_color) and not currently_highest.is_trump(trump_color):
                return True
            elif not self.is_trump(trump_color) and currently_highest.is_trump(trump_color):
                return False
            elif self.color != following_suit:  # we can assume the currently highest card is following the suit. 
                return False
            else:
                return self.number > currently_highest.number
        else:
            raise TypeError(f"The currently highest card has an unexpected type: {type(currently_highest)}!")
            
    def is_playable(self, player_cards: Collection["Card"], following_suit: Optional[Color]) -> bool:
        if following_suit is None:
            return True
        if following_suit == self.color:
            return True
        if all(card.color != following_suit for card in player_cards if isinstance(card, ColoredCard)):
            return True
        return False
    
    def is_trump(self, trump_color: TrumpColor) -> bool:
        return self.color.value == trump_color.value

    def __str__(self) -> str:
        return f"{self.color.value[:1]}{self.number}"

    def __repr__(self) -> str:
        return f"{self.color.value[:1]}{self.number}"


class Wizard(Card):
    def is_highest(self, currently_highest: Optional["Card"],
                   following_suit: Optional[Color], trump_color: TrumpColor) -> bool:
        return currently_highest is None or not isinstance(currently_highest, Wizard)

    def is_playable(self, player_cards: Collection["Card"], following_suit: Optional[Color]) -> bool:
        return True

    def __str__(self) -> str:
        return "wizard"

    def __repr__(self) -> str:
        return "wizard"


class Jester(Card):
    def is_highest(self, currently_highest: Optional["Card"],
                   following_suit: Optional[Color], trump_color: TrumpColor) -> bool:
        return currently_highest is None or isinstance(currently_highest, Jester)

    def is_playable(self, player_cards: Collection["Card"], following_suit: Optional[Color]) -> bool:
        return True

    def __str__(self) -> str:
        return "jester"

    def __repr__(self) -> str:
        return "jester"


def get_all_cards() -> list[Card]:
    cards: list[Card] = []
    for number in range(MIN_NUMBER, MAX_NUMBER + 1):
        for color in Color:
            cards.append(ColoredCard(number, color))
    for _ in range(NUM_JESTERS):
        cards.append(Jester())

    for _ in range(NUM_WIZARDS):
        cards.append(Wizard())
    return cards
