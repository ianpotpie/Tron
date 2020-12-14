import numpy as np
from bot_algorithms.ian_alpha_beta_cutoff import alpha_beta_cutoff
from bot_algorithms.voronoi_heuristic import *
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
from bot_algorithms.alpha_beta_cutoff_2 import alpha_beta_cutoff2, voronoi
from gamerunner import run_game
from bots import StudentBot, StudentBot2


def main():
    best_score = 0
    weights = [1, 1, 1, 1]

    for episode in range(1000):

        for i in range(4):
            wins = 0
            weights[i] += 1
            for _ in range(100):
                wins += run_game(TronProblem, [StudentBot, StudentBot2(weights)], None, 0.2, 0.3, True)[1]
            if (wins / 100) < best_score:
                weights[i] -= 1
            else:
                best_score = (wins / 100)
                print(weights)


if __name__ == "__main__":
    main()