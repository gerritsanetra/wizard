import logging
from random import Random
from uuid import uuid4

from wizard.card import get_all_cards, ColoredCard, Jester, Wizard, Card
from wizard.color import TrumpColor
from wizard.constants import MIN_PLAYERS_NUM, MAX_PLAYERS_NUM
from wizard.player.player import Player
from wizard.trick import simulate_trick
LOGGER = logging.getLogger(__name__)


class WizardGame:
    def __init__(self, players: list[Player], seed: int) -> None:
        if not(MIN_PLAYERS_NUM <= len(players) <= MAX_PLAYERS_NUM):
            raise ValueError(f"A wizard game supports {MIN_PLAYERS_NUM} to {MAX_PLAYERS_NUM} players, "
                             f"but {len(players)} were given.")
        self.uuid = str(uuid4())
        self.players = players
        self.random = Random(seed)

    def simulate_rounds(self):
        num_rounds = self.get_num_rounds()
        cumulated_scores: dict[Player, int] = {player: 0 for player in self.players}
        LOGGER.info(f"Starting game {self.uuid}", extra={"game": self.uuid})
        for round_idx in range(num_rounds):
            LOGGER.info(f"Starting round {round_idx}", extra={"game": self.uuid, "round_idx": round_idx})
            scores = self.simulate_round(round_idx)
            for player in self.players:
                cumulated_scores[player] += scores[player]
            LOGGER.info(f"cumulated_scores: {cumulated_scores}", extra={"game": self.uuid, "round_idx": round_idx})
        return cumulated_scores

    def get_num_rounds(self):
        return len(get_all_cards()) // len(self.players)

    def simulate_round(self, round_idx: int) -> dict[Player, int]:
        all_cards = get_all_cards()
        cards_num = round_idx + 1
        players_in_order = self.get_players_in_order(cards_num)

        self.distribute_cards(all_cards, cards_num, players_in_order)

        bidden_tricks = self.simulate_bidding(cards_num, players_in_order)
        LOGGER.info(f"bidden_tricks: {bidden_tricks}", extra={"game": self.uuid, "round_idx": round_idx})
        trump_color = self.get_trump_color(all_cards, cards_num, players_in_order)
        taken_tricks = self.simulate_tricks(bidden_tricks, cards_num, players_in_order, trump_color)
        LOGGER.info(f"taken_tricks: {taken_tricks}", extra={"game": self.uuid, "round_idx": round_idx})
        scores = self.get_scores(bidden_tricks, players_in_order, taken_tricks)
        LOGGER.info(f"scores: {scores}", extra={"game": self.uuid, "round_idx": round_idx})

        first_player = self.players[0]
        for player in self.players:
            if len(player.cards) != len(first_player.cards):
                raise RuntimeError("Something went wrong!")

        return scores

    def distribute_cards(self, all_cards: list[Card], cards_num: int, players_in_order: list[Player]):
        self.random.shuffle(all_cards)
        for player_idx, player in enumerate(players_in_order):
            player.cards = []
            for card_idx in range(cards_num):
                player.cards.append(all_cards[player_idx * cards_num + card_idx])

    @classmethod
    def simulate_bidding(cls, cards_num: int, players_in_order: list[Player]):
        bidden_tricks: dict[Player, int] = {}
        allowed_bids = list(range(cards_num + 1))
        for player in players_in_order[:-1]:
            bidden_tricks[player] = player.bid_tricks(allowed_bids)
        dealer = players_in_order[-1]
        sum_of_bids = sum(bid for bid in bidden_tricks.values())
        if cards_num - sum_of_bids >= 0:
            allowed_bids.remove(cards_num - sum_of_bids)
        bidden_tricks[dealer] = dealer.bid_tricks(allowed_bids)
        return bidden_tricks

    @classmethod
    def get_trump_color(cls, all_cards: list[Card], cards_num: int, players_in_order: list[Player]):
        trump_determining_card_idx = cards_num * len(players_in_order) + 1
        dealer = players_in_order[-1]
        if len(all_cards) <= trump_determining_card_idx:
            trump_color = TrumpColor.NO_TRUMP
        else:
            trump_determining_card = all_cards[trump_determining_card_idx]
            if isinstance(trump_determining_card, ColoredCard):
                trump_color = trump_determining_card.color
            elif isinstance(trump_determining_card, Jester):
                trump_color = TrumpColor.NO_TRUMP
            elif isinstance(trump_determining_card, Wizard):
                trump_color = dealer.choose_trump_color()
                if trump_color == TrumpColor.NO_TRUMP:
                    raise ValueError(f"The dealer {dealer} chose no trump as the trump color which is not allowed!")
            else:
                raise TypeError(f"Unexpected type {type(trump_determining_card)}!")
        return trump_color

    @classmethod
    def simulate_tricks(cls,
                        bidden_tricks: dict[Player, int],
                        cards_num: int,
                        players_in_order: list[Player],
                        trump_color: TrumpColor) -> dict[Player, int]:
        taken_tricks: dict[Player, int] = {player: 0 for player in players_in_order}
        for trick_idx in range(cards_num):
            winner = simulate_trick(
                players=players_in_order,
                trump_color=trump_color,
                bidden_tricks=bidden_tricks,
                taken_tricks=taken_tricks,
            )
            taken_tricks[winner] = taken_tricks[winner] + 1
        return taken_tricks

    @classmethod
    def get_scores(cls,
                   bidden_tricks: dict[Player, int],
                   players_in_order: list[Player],
                   taken_tricks: dict[Player, int]):
        scores: dict[Player, int] = {}
        for player in players_in_order:
            if bidden_tricks[player] == taken_tricks[player]:
                scores[player] = bidden_tricks[player] * 10 + 20
            else:
                scores[player] = abs(bidden_tricks[player] - taken_tricks[player]) * -10
        return scores

    def get_players_in_order(self, cards_num: int) -> list[Player]:
        players_in_order: list[Player] = []
        dealer_idx = (cards_num - 1) % len(self.players)
        if dealer_idx != len(self.players) - 1:
            players_in_order.extend(self.players[dealer_idx + 1:])
        if dealer_idx != 0:
            players_in_order.extend(self.players[:dealer_idx])
        players_in_order.append(self.players[dealer_idx])
        return players_in_order
