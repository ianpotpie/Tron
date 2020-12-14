#!/usr/bin/python

import numpy as np
from bot_algorithms.ian_alpha_beta_cutoff import alpha_beta_cutoff
from bot_algorithms.voronoi_heuristic import *
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
from bot_algorithms.alpha_beta_cutoff_2 import alpha_beta_cutoff2, voronoi

cutoff = 8

class StudentBot1:
    """ Write your student bot here"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        # direction = alpha_beta_cutoff2(asp, 5)
        direction = alpha_beta_cutoff(asp, cutoff, voronoi_v2)
        return direction
        # return "U"




        #Performance cutoffs




        # results:
        # arjun alpha beta, arjun voronoi:
        # ian alpha beta, ian vornoi:
        # arjun alpha beta, ian voronoi
        # ian alpha beta, arjun vornoi:
        # arjun alpha beta with special voronoi:
        # ian alpha beta with special
        # special alpha beta with arjun voronoi:
        # special alpha beta with ian voronoi



    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass

class StudentBot2:
    """ Write your student bot here"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        # direction = alpha_beta_cutoff2(asp, 5)
        direction = alpha_beta_cutoff(asp, cutoff, voronoi_v3)
        return direction
        # return "U"




        #Performance cutoffs




        # results:
        # arjun alpha beta, arjun voronoi:
        # ian alpha beta, ian vornoi:
        # arjun alpha beta, ian voronoi
        # ian alpha beta, arjun vornoi:
        # arjun alpha beta with special voronoi:
        # ian alpha beta with special
        # special alpha beta with arjun voronoi:
        # special alpha beta with ian voronoi



    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass

class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
