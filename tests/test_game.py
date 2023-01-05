from wizard.game import WizardGame


def test_two_players_game(two_players_game: WizardGame) -> None:
    print(two_players_game.simulate_rounds())


def test_six_players_game(six_players_game: WizardGame) -> None:
    print(six_players_game.simulate_rounds())
