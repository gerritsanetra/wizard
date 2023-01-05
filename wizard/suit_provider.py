from typing import Optional

from wizard.card import Card, ColoredCard, Wizard
from wizard.color import Color


def get_suit(following_suit: Optional[Color], played_cards: list[Card]) -> Optional[Color]:
    if following_suit is not None:
        return following_suit
    if len(played_cards) == 0:
        return None
    for played_card in played_cards:
        if isinstance(played_card, ColoredCard):
            return played_card.color
        elif isinstance(played_card, Wizard):
            return None
    return None
