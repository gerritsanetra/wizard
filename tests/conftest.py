import pytest

from wizard.game import WizardGame
from wizard.player.player import Player
from wizard.player.random_player import RandomPlayer


@pytest.fixture(scope="function")
def players() -> list[Player]:
    return [
        RandomPlayer(seed=42, name="gerrit"),
        RandomPlayer(seed=43, name="sven"),
        RandomPlayer(seed=44, name="max"),
        RandomPlayer(seed=45, name="jan"),
        RandomPlayer(seed=45, name="marius"),
        RandomPlayer(seed=45, name="julian"),
    ]


@pytest.fixture(scope="function")
def two_players_game(players: list[Player]) -> WizardGame:
    return WizardGame(
        players=players[:2],
        seed=46,
    )


@pytest.fixture(scope="function")
def six_players_game(players: list[Player]) -> WizardGame:
    return WizardGame(
        players=players[:6],
        seed=47,
    )