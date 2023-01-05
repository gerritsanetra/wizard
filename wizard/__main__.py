import logging

from wizard.game import WizardGame
from wizard.player.random_player import RandomPlayer
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    players = [
        RandomPlayer(seed=42, name="gerrit"),
        RandomPlayer(seed=43, name="sven"),
        RandomPlayer(seed=44, name="max"),
        # RandomPlayer(seed=45, name="jan"),
        # RandomPlayer(seed=45, name="marius"),
        # RandomPlayer(seed=45, name="julian"),
    ]
    game = WizardGame(players=players, seed=46)
    scores = game.simulate_rounds()
    LOGGER.info(f"Final scores: {scores}", extra={"game": game.uuid})
