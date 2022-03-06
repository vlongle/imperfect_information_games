from typing import Sequence

from imperfect_info_games.games.game import ExtensiveFormGame
from imperfect_info_games.player import Player
from imperfect_info_games.utils import lessVerboseEnum


class ROCK_PAPER_SCISSOR_ACTIONS(lessVerboseEnum):
    """Available actions for the rock-paper-scissors game."""
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class RockPaperScissorGame(ExtensiveFormGame):
    """A rock-paper-scissor (extensive-form) game."""

    def __init__(self, players: Sequence[Player]):
        assert len(players) == 2
        super().__init__(players)
        self.actions = ROCK_PAPER_SCISSOR_ACTIONS

    def get_active_player(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Player:
        if len(history) == 0:
            return self.players[0]
        elif len(history) == 1:
            return self.players[1]
        else:
            raise ValueError("Invalid history " + str(history))

    def is_terminal(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> bool:
        return len(history) == 2

    def get_payoffs(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Sequence[float]:
        assert self.is_terminal(history)
        if len(history) > 2:
            raise ValueError("Invalid history " + str(history))

        history_str = self.history_to_str(history)
        match history_str:
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [1, -1]
            case "PAPER-ROCK":
                return [1, -1]
            case "PAPER-SCISSOR":
                return [-1, 1]
            case "SCISSOR-ROCK":
                return [-1, 1]
            case "SCISSOR-PAPER":
                return [1, -1]
        return [0, 0]

    def get_infostate(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> str:
        if len(history) == 0:
            return "P0"
        elif len(history) == 1:
            return "P1"
        else:
            raise ValueError("Invalid history " + str(history))

# def play_against_fixed_policy():
#     """
#     regret-matching agent plays against a fixed policy agent in
#     rock-paper-scissor.
#     """
#     n_steps = 10000
#     regret_matching = RegretMatchingAgent(
#         name='regret matching', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     opponent_policy = np.array([1/3, 1/3, 1/3])
#     #opponent_policy = np.array([0.34, 0.33, 0.33])
#     fixed_opponent = FixedPolicyAgent("fixed_opponent", opponent_policy)
#     agents = [regret_matching, fixed_opponent]
#     game = RockPaperScissorGame(agents, n_steps=n_steps)
#     game.run()
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# def play_against_regret_matching():
#     """
#     both agents are regret-matching agents.
#     Their avg policies should both converge to a Nash equilibrium,
#     which is [1/3, 1/3, 1/3] for rock-paper-scissor.
#     """
#     n_steps = 10000
#     regret_matching_1 = RegretMatchingAgent(
#         name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     regret_matching_2 = RegretMatchingAgent(
#         name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     agents = [regret_matching_1, regret_matching_2]
#     game = RockPaperScissorGame(agents, n_steps=n_steps)
#     game.run()
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# def play_against_delay_regret_matching():
#     """
#     both agents are regret-matching agents. We delay the policy update of one agent
#     while updating the other for several games.
#     Their avg policies should both converge to a Nash equilibrium,
#     which is [1/3, 1/3, 1/3] for rock-paper-scissor.
#     """
#     n_steps = 10000
#     freeze_interval = 50
#     freeze_duration = n_steps // freeze_interval  # no. of games per freeze interval
#     regret_matching_1 = RegretMatchingAgent(
#         name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     regret_matching_2 = RegretMatchingAgent(
#         name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     agents = [regret_matching_1, regret_matching_2]
#     game = RockPaperScissorGame(agents, n_steps=freeze_duration)
#     for _ in range(freeze_interval):
#         # evolve first agent, freeze 2nd
#         game.run(freeze_ls=[regret_matching_2])
#         # evolve second agent, freeze 1st
#         game.run(freeze_ls=[regret_matching_1])
#
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# if __name__ == '__main__':
#     play_against_delay_regret_matching()
#     # play_against_fixed_policy()
#     # play_against_regret_matching()