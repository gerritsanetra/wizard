from typing import Optional

from wizard.card import Card
from wizard.color import Color, TrumpColor
from wizard.player.player import Player
from wizard.suit_provider import get_suit


def simulate_trick(
        players: list[Player],
        trump_color: TrumpColor,
        bidden_tricks: dict[Player, int],
        taken_tricks: dict[Player, int],
) -> Player:
    played_cards: list[Card] = []
    currently_highest: Optional[Card] = None
    following_suit: Optional[Color] = None
    cards_players: dict[Card, Player] = {}
    for player in players:
        played_card = player.play_next_card(
            played_cards=played_cards,
            currently_highest=currently_highest,
            following_suit=following_suit,
            trump_color=trump_color,
            cards_players=cards_players,
            players=players,
            bidden_tricks=bidden_tricks,
            taken_tricks=taken_tricks,
        )
        if not played_card.is_playable(player.cards, following_suit):
            raise ValueError(f"The player {player} wanted to play {played_card} in response to {played_cards}!")
        player.cards.remove(played_card)
        cards_players[played_card] = player
        played_cards.append(played_card)
        following_suit = get_suit(following_suit, played_cards)
        if played_card.is_highest(currently_highest, following_suit, trump_color):
            currently_highest = played_card
    return cards_players[currently_highest]
