import numpy as np
from bot_algorithms.alpha_beta_cutoff import alpha_beta_cutoff
from bot_algorithms.voronoi_heuristic import *
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math

from gamerunner import run_game



def optimize():
    best_score = 0
    weights = [1, 1, 1, 1]

    for episode in range(1000):

        for i in range(4):
            wins = 0
            weights[i] += 1
            for _ in range(100):
                tron_problem = TronProblem("maps/empty_room.txt", 0)
                student_bot = StudentBot()
                student_bot_2 = StudentBot2(weights)


                wins += run_game(tron_problem, [student_bot, student_bot_2], None, 0.2, 0.3, True)[1]
            if (wins / 100) < best_score:
                weights[i] -= 1
            else:
                best_score = (wins / 100)
                print(weights)


if __name__ == "__main__":
    print("l")
    optimize()