import numpy as np
import math

# this heuristic is absolutely terrible, but now it works

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def naive_voronoi(state):

    player_to_move = state.ptm
    num_players = len(state.player_locs)
    player_score = 0

    free_cells = 0
    for cell_y, row in enumerate(state.board):
        for cell_x, cell in enumerate(row):
            if cell == ' ':
                free_cells += 1
                closest_players = []
                min_dist = math.inf
                # find the set of players closest to the cell
                for player in range(num_players):
                    player_x = state.player_locs[player][0]
                    player_y = state.player_locs[player][1]
                    curr_dist = manhattan_distance(player_x, player_y, cell_x, cell_y)
                    if curr_dist < min_dist:
                        closest_players = [player]
                        min_dist = curr_dist
                    elif curr_dist == min_dist:
                        closest_players.append(player)
                # if the player to move is in the list, then add to their score proportionaly
                if player_to_move in closest_players:
                    player_score += 1/len(closest_players)

    # normalize the score for adversarial search (so the net score for all players is zero)
    player_score -= (free_cells/num_players)
    return player_score

