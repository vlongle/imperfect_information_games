import logging

import click
import numpy as np

from imperfect_info_games.algos.cfr import (
    CounterFactualRegretMinimizerPlayer,
    counterfactualRegretMinimizerTrainer,
)
from imperfect_info_games.games.bar_crowding import BarCrowdingGame
from imperfect_info_games.games.kuhn_poker import KuhnPokerGame
from imperfect_info_games.games.prisoner_dilemma import PrisonerDilemmaGame
from imperfect_info_games.games.rock_paper_scissor import (
    AsymmetricRockPaperScissorGame,
    RockPaperScissorGame,
)


np.random.seed(0)


@click.command()
@click.option("--game", type=click.Choice(["RockPaperScissorGame", "AsymmetricRockPaperScissorGame", "BarCrowdingGame", "PrisonerDilemmaGame", "KuhnPokerGame", ]),
              default="RockPaperScissorGame", help="The game to demo.")
@click.option("--n_iters", type=int, default=10000, help="The number of iterations to run the game for.")
@click.option("--verbose_level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]), default="INFO", help="The verbosity level of the game.")
def main(game: str, n_iters: int = 10000, verbose_level: str = "INFO"):
    """Demo for CounterFactualRegretMinimizer (CFR) algorithm for extensive-form games.

    Available games:
    ----------------

    RockPaperScissorGame, AsymmetricRockPaperScissorGame, BarCrowdingGame, PrisonerDilemmaGame, KuhnPokerGame

    Available options:
    ------------------

        --game: The game to demo.
        --n_iters: The number of iterations to run the game for.
    """
    logging.basicConfig(level=getattr(
        logging, verbose_level), format="%(message)s")
    Game_dict = {
        "RockPaperScissorGame": RockPaperScissorGame,
        "AsymmetricRockPaperScissorGame": AsymmetricRockPaperScissorGame,
        "BarCrowdingGame": BarCrowdingGame,
        "PrisonerDilemmaGame": PrisonerDilemmaGame,
        "KuhnPokerGame": KuhnPokerGame,
    }
    Game = Game_dict[game]
    players = [CounterFactualRegretMinimizerPlayer(
        f"cfr{i}", i) for i in range(Game.n_players)]
    cfr_solver = counterfactualRegretMinimizerTrainer(
        Game(players), n_iters=n_iters)
    cfr_solver.train()


if __name__ == "__main__":
    main()