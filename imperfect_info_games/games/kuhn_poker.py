'''
Kuhn Poker.
- Two players
- Three cards: 1,2,3
- Each player gets a random card
- On a turn, a player can either
    - pass: do nothing. The opponent takes all chip in the pot
    - bet: place a chip in the pot
- after two passes or two bets (not necessarily consecutive), the game ends. Player with the highest card wins.
- Maximum depth of the game tree is 3.

Game tree.
        [chance]
           |
      assign cards
           |
        [player1]
        /      \
    pass        bet
     |           |
  [player2]       [player2]
    /   \\         /   \
  pass    bet   pass     bet
   |      |       |         |
   (h)  [player1]   (1)       (h)
        /   \
      pass   bet
        |     |
        (2)   (h)
Leaf nodes:
    (h) - player has highest card wins!
    (1) - player 1 wins! (player 2 chickens out)
    (2) - player 2 wins! (player 1 chickens out)

Information set: is a set of decision nodes of the decision-making player that are indistinguishable to that player.
In our game, we have 12 info-sets. Each info-set has 2 states since the opponent can have any of the two cards that I'm not already holding. We have 6 ways to deal 2 out of 3 cards to 2 players, and 2 states / info-set so we have 6/2 = 3 info sets at every decision node. We have 4 decision nodes so 3 * 4 = 12 info sets.
NOTE the subtle difference between the no. of info sets and the no. of nodes per info set. (the size of the info set). The size of the info. set tells us how many worlds are consistent with the player's observations so far. The no. of info sets is more "meta". The player, without entering into a game / trajectory, can reason ahead about the different info. sets that they can be in once some partial observations are available to them when the game starts.

We will use Counterfactual Regret Minimization (CFR) that extends rock-paper-scissor regret-matching.

Notation:
    - sigma: policy
    - h: history i.e. sequence of actions taken by players and chance
    - pi(h | sigma) : reach probability of a particular history given a policy

==============================================================================================================================
Question: Why do we need to multiply by counterfactual reach probability to calculate regret???

https://cs.stackexchange.com/questions/132738/in-counterfactual-regret-minimization-why-are-additions-to-regret-weighted-by-r

So that we can take into account average and stuff...
In fact, this approach is very similar to advantage function in Q-learning

https://escholarship.org/content/qt9178b2q6/qt9178b2q6.pdf?t=ppfl6c
In fact, this paper writes cfr as advantage-function-like RL form!!


So, we have established that weighting the contribution to info-set-wide regret by each hist (realized in different games) by the reach probability to that history is important to differentiate
different contributions to info-set-wide strategy by different paths with different probs

BUT, why do we use opponent's prob in reach prob. without also factoring our own? I guess we can put in our own prob. if we really want to but it's not neccessary?? Or maybe even undesirable as our strat changes...
'''
from enum import Enum
from enum import IntEnum
from typing import Sequence

import numpy as np

from imperfect_info_games.games.game import ExtensiveFormGame
from imperfect_info_games.player import Player
from imperfect_info_games.utils import lessVerboseEnum


class KUHN_POKER_ACTIONS(lessVerboseEnum, IntEnum):
    PASS = 0
    BET = 1


class KUHN_POKER_CHANCE_ACTIONS(lessVerboseEnum, IntEnum):
    """
    3 cards J, Q, K dealt randomly to 2 players.
    """
    JQ = 0  # player 2 wins
    JK = 1  # player 2 wins
    QK = 2  # player 2 wins
    QJ = 3  # player 1 wins
    KJ = 4  # player 1 wins
    KQ = 5  # player 1 wins


class KuhnPokerGame(ExtensiveFormGame):
    """
    TODO: add documentation
    """
    actions = KUHN_POKER_ACTIONS
    chance_actions = KUHN_POKER_CHANCE_ACTIONS
    n_players = 2
    has_chance_player = True

    def is_terminal(self, history: Sequence[IntEnum]):
        history_str = self.history_to_str(history[1:])  # ignore chance node
        terminal_nodes = ["PASS-PASS", "BET-BET", "BET-PASS",
                          "PASS-BET-PASS", "PASS-BET-BET"]
        return history_str in terminal_nodes

    def get_active_player(self, history: Sequence[IntEnum]) -> Player:
        return self.players[(len(history)-1) % 2]

    def get_winner(self, chance_action: KUHN_POKER_CHANCE_ACTIONS) -> int:
        if chance_action.value < 3:
            return 1
        return 0

    def showdown(self, history):
        """
        Return the payoff value ASSUMING that the pot contains 2 chips
        """
        winner = self.get_winner(history[0])
        return np.array([1, -1]) if winner == 0 else np.array([-1, 1])

    def get_payoffs(self, history):
        """
        This game has 5 terminal nodes
        """
        assert self.is_terminal(history)
        match '-'.join(map(str, history[1:])):
            case "PASS-PASS":
                return 1 * self.showdown(history)  # wins 2 chips
            case "BET-BET":
                return 2 * self.showdown(history)  # wins 4 chips
            case "BET-PASS":
                return np.array([1, -1])  # player 2 forfeits, player 1 wins
            case "PASS-BET-PASS":
                return np.array([-1, 1])  # player 1 forfeits, player 2 wins
            case "PASS-BET-BET":
                return 2 * self.showdown(history)  # wins 4 chips
        raise Exception("Invalid history")

    def get_card(self, chance_action: KUHN_POKER_CHANCE_ACTIONS, player_id: int) -> str:
        return chance_action.name[player_id]

    def get_infostate(self, history: Sequence[Enum]) -> str:
        player_id = self.get_active_player(history).player_id  # type: ignore
        my_card = self.get_card(history[0], player_id)  # type: ignore
        return my_card + "-" + "-".join(map(str, history[1:]))

    def chance_action(self) -> KUHN_POKER_CHANCE_ACTIONS:
        return KUHN_POKER_CHANCE_ACTIONS(np.random.choice(range(len(KUHN_POKER_CHANCE_ACTIONS))))

    @staticmethod
    def shorten_history(history_str: str) -> str:
        """Shorten history string. For example, "KJ-PASS-BET" -> "KJPB".
        Args:
            - history_str: history string

        Returns:
            - shortened history string
        """
        s = ''.join(str(a) for a in history_str)
        replacements = {'-': '', 'PASS': 'P', 'BET': 'B'}
        for k, v in replacements.items():
            s = s.replace(k, v)
        return s + ' ' * (5-len(s))