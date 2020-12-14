import numpy as np
import math
from queue import PriorityQueue


# this heuristic is absolutely terrible, but now it works

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def naive_voronoi(state):
    """
    Input:
        A state
    Returns:
        The score of the game for the player who is about to move based on a naive voronoi metric. The naive voronoi
        metric does not account for walls and simply counts the closest open spaces for each player.
    """

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
                    player_x = state.player_locs[player][1]
                    player_y = state.player_locs[player][0]
                    curr_dist = manhattan_distance(player_x, player_y, cell_x, cell_y)
                    if curr_dist < min_dist:
                        closest_players = [player]
                        min_dist = curr_dist
                    elif curr_dist == min_dist:
                        closest_players.append(player)
                # if the player to move is in the list, then add to their score proportionally
                if player_to_move in closest_players:
                    player_score += 1 / len(closest_players)

    # normalize the score for adversarial search (so the net score for all players is zero)
    player_score -= (free_cells / num_players)
    return player_score


########################################################################################################################


def voronoi_v1(state, curr_player):
    """
    Input:
        A Game State
    Output:
        The Score of the player to move based on the voronoi metric. This cycles through the players in the order of
        the their turns to avoid conflicting frontiers (from evaluating at the same time).
    """

    # initialize game info
    player_locs = state.player_locs
    num_players = len(player_locs)
    board = state.board

    # initialize the voronoi cells for each player with the cell that they currently occupy
    voronoi_sets = [{(loc[0], loc[1])} for loc in player_locs]

    # initialize the frontiers with the coordinates of the cells surrounding each player
    frontier_sets = \
        [{(loc[0] + 1, loc[1]),
          (loc[0] - 1, loc[1]),
          (loc[0], loc[1] + 1),
          (loc[0], loc[1] - 1)} for loc in player_locs]

    # We cycle through the players in the order that their turns will take place. We begin with the player who is about
    # to move. We know we are done when there are no cells left to explore
    expanding_player = curr_player
    empty_frontiers = 0
    while empty_frontiers < num_players:
        next_frontier = set()
        # adds the frontier to the voronoi space, and expands where it can
        for cell in frontier_sets[expanding_player]:
            # get the cell info
            cell_row = cell[0]
            cell_col = cell[1]
            cell_val = board[cell_row][cell_col]

            # if the cell is available, then it is added to the voronoi and expand the frontier
            if (not any([cell in voronoi for voronoi in voronoi_sets])) \
                    and (cell_val != 'x') and (cell_val != '#'):
                voronoi_sets[expanding_player].add(cell)
                next_frontier.add((cell_row + 1, cell_col))
                next_frontier.add((cell_row - 1, cell_col))
                next_frontier.add((cell_row, cell_col + 1))
                next_frontier.add((cell_row, cell_col - 1))

        # update the frontier and begin calculating the voronoi space of the new
        frontier_sets[expanding_player] = next_frontier
        if len(next_frontier) == 0:
            empty_frontiers += 1
        else:
            empty_frontiers = 0
        expanding_player = (expanding_player + 1) % num_players

    # the player's score is tallied by taking the difference between the size of their voronoi, and
    # the sum of the sizes of all the other player's voronoi spaces
    player_score = 0
    for player, voronoi in enumerate(voronoi_sets):
        if player == curr_player:
            player_score += len(voronoi)
        else:
            player_score -= len(voronoi)

    print(player_score)
    return player_score


########################################################################################################################


def voronoi_v2(state, curr_player):
    """
    Input:
        A Game State
    Output:
        The Score of the player to move based on the voronoi metric. This cycles through the players in the order of
        the their turns to avoid conflicting frontiers (from evaluating at the same time).
    """

    # initialize game info
    player_locs = state.player_locs
    num_players = len(player_locs)
    voronoi_sizes = np.zeros(num_players)
    board = state.board

    # initialize the voronoi cells for each player with the cell that they currently occupy
    explored_cells = set(player_locs)

    # initialize the frontiers with the coordinates of the cells surrounding each player
    frontier_sets = [{(loc[0], loc[1])} for loc in player_locs]

    # We cycle through the players in the order that their turns will take place. We begin with the player who is about
    # to move. We know we are done when there are no cells left to explore
    expanding_player = curr_player
    empty_frontiers = 0
    while empty_frontiers < num_players:
        next_frontier = set()
        # adds the frontier to the voronoi space, and expands where it can
        for cell in frontier_sets[expanding_player]:
            explored_cells.add(cell)
            voronoi_sizes[expanding_player] += 1

            def viable_cell(cell_row, cell_col):
                val = board[cell_row][cell_col]
                return ((cell_row, cell_col) not in explored_cells) and (val != 'x') and (val != '#')

            row = cell[0]
            col = cell[1]

            # if the cell is available, then it is added to the voronoi and expand the frontier
            if viable_cell(row+1, col):
                next_frontier.add((row + 1, col))
            if viable_cell(row-1, col):
                next_frontier.add((row - 1, col))
            if viable_cell(row, col+1):
                next_frontier.add((row, col + 1))
            if viable_cell(row, col-1):
                next_frontier.add((row, col - 1))

        # update the frontier and begin calculating the voronoi space of the new
        frontier_sets[expanding_player] = next_frontier
        if len(next_frontier) == 0:
            empty_frontiers += 1
        else:
            empty_frontiers = 0
        expanding_player = (expanding_player + 1) % num_players

    # the player's score is tallied by taking the difference between the size of their voronoi, and
    # the sum of the sizes of all the other player's voronoi spaces
    player_score = 0
    for player, size in enumerate(voronoi_sizes):
        if player == curr_player:
            player_score += size
        else:
            player_score -= size / (num_players - 1)

    return player_score

########################################################################################################################


def voronoi_v3(state, curr_player):
    """
    Input:
        A Game State
    Output:
        The Score of the player to move based on the voronoi metric. This cycles through the players in the order of
        the their turns to avoid conflicting frontiers (from evaluating at the same time).
    """

    # initialize game info
    player_locs = state.player_locs
    num_players = len(player_locs)
    voronoi_values = np.zeros(num_players)
    board = state.board

    # initialize the voronoi cells for each player with the cell that they currently occupy
    explored_cells = set(player_locs)

    # initialize the frontiers with the coordinates of the cells surrounding each player
    frontier_sets = [{(loc[0], loc[1])} for loc in player_locs]

    # We cycle through the players in the order that their turns will take place. We begin with the player who is about
    # to move. We know we are done when there are no cells left to explore
    expanding_player = curr_player
    empty_frontiers = 0
    while empty_frontiers < num_players:
        next_frontier = set()
        # adds the frontier to the voronoi space, and expands where it can
        for cell in frontier_sets[expanding_player]:
            explored_cells.add(cell)

            def viable_cell(cell_row, cell_col):
                val = board[cell_row][cell_col]
                return ((cell_row, cell_col) not in explored_cells) and (val != 'x') and (val != '#')

            row = cell[0]
            col = cell[1]

            # if the cell is available, then it is added to the voronoi and expand the frontier
            open_neighbors = 0
            if viable_cell(row+1, col):
                next_frontier.add((row + 1, col))
                open_neighbors += 1
            if viable_cell(row-1, col):
                next_frontier.add((row - 1, col))
                open_neighbors += 1
            if viable_cell(row, col+1):
                next_frontier.add((row, col + 1))
                open_neighbors += 1
            if viable_cell(row, col-1):
                next_frontier.add((row, col - 1))
                open_neighbors += 1

            if open_neighbors == 3:
                voronoi_values[expanding_player] += 4
            elif open_neighbors == 2:
                voronoi_values[expanding_player] += 4
            elif open_neighbors == 1:
                voronoi_values[expanding_player] += 4
            elif open_neighbors == 0:
                voronoi_values[expanding_player] += 1

        # update the frontier and begin calculating the voronoi space of the new
        frontier_sets[expanding_player] = next_frontier
        if len(next_frontier) == 0:
            empty_frontiers += 1
        else:
            empty_frontiers = 0
        expanding_player = (expanding_player + 1) % num_players

    # the player's score is tallied by taking the difference between the size of their voronoi, and
    # the sum of the sizes of all the other player's voronoi spaces
    player_score = 0
    for player, size in enumerate(voronoi_values):
        if player == curr_player:
            player_score += size
        else:
            player_score -= size / (num_players - 1)

    return player_score

