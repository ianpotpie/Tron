import numpy as np
import math
from queue import PriorityQueue


def alpha_beta_cutoff2(asp, cutoff_ply):
    """
    This function should:
    - search through the asp using alpha-beta pruning
    - cut off the search after cutoff_ply moves have been made.

    Inputs:
            asp: a TronProblem
            cutoff_ply: how deep to search

    Output: an action (U, D, L, R)

    TODO: IMPLEMENT A TIME COUNTER (with some margin for error)
    TODO: give an action that doesn't kill us whenever possible!!
    """
    state = asp.get_start_state()
    player = state.player_to_move()
    actions = asp.get_available_actions(state)
    alpha = float("-inf")  # represents hightest max value
    beta = float("inf")  # represents lowest min value
    best_action = actions.pop()
    actions.add(best_action)
    for action in actions:
        payoff = min_value_ab_cutoff(asp, asp.transition(state, action), player, alpha, beta, cutoff_ply - 1)
        if payoff > alpha:
            alpha = payoff
            best_action = action
            # print(best_action)
    return best_action  # TODO: give an action that doesn't kill us if possible
    # (even if we've already lost against an optimal bot, we want to stay alive)


def min_value_ab_cutoff( asp, state, player, alpha, beta, cutoff_ply):
    # helper function for alpha_beta
    if asp.is_terminal_state(state):
        return (asp.evaluate_state(state)[player] * 500) - 250
    if cutoff_ply <= 0:
        return voronoi(state, player)
    actions = asp.get_available_actions(state)
    min_payoff = float('inf')
    for action in actions:
        min_payoff = min(min_payoff, max_value_ab_cutoff(asp, asp.transition(state, action), player, alpha, beta, cutoff_ply - 1))
        if min_payoff < alpha:
            return min_payoff
        beta = min(beta, min_payoff)
    return min_payoff


def max_value_ab_cutoff( asp, state, player, alpha, beta, cutoff_ply):
    # helper function for alpha_beta
    if asp.is_terminal_state(state):
        return (asp.evaluate_state(state)[player] * 500) - 250
    if cutoff_ply <= 0:
        return voronoi(state, player)
    actions = asp.get_available_actions(state)
    max_payoff = float('-inf')
    for action in actions:
        max_payoff = max(max_payoff, min_value_ab_cutoff(asp, asp.transition(state, action), player, alpha, beta, cutoff_ply - 1))
        if max_payoff > beta:
            return max_payoff
        alpha = max(alpha, max_payoff)
    return max_payoff


def voronoi(state, player):
    """
    Input: state, a state in a TronProblem. player, index for player in game
    Output: number represneting voronoi heuristic evaluation of state
    for the given player. Positive is good for the given player

    """
    distances = calc_distances(state)  # distances from each player to each square, flattened matrix
    # print(distances[1] - distances[0])
    distance_diff = distances[0] - distances[1]
    # board = state.board
    # s = ""
    # for row in board:
    #     for cell in row:
    #         s += cell
    #     s += "\n"
    # print("testing board: " + str(s))

    voronoi = 0
    for i in range(len(distance_diff)):
        if ((distances[0])[i] >= 0) and ((distances[1])[i] == -1):  # if p1 can get there but p2 can't
            voronoi += 1
        elif ((distances[1])[i] >= 0) and ((distances[0])[i] == -1):  # if p2 can get there but p1 can't
            voronoi -= 1
        elif distance_diff[i] < 0:  # if p1 gets there in less time
            voronoi += 1
        elif distance_diff[i] > 0:  # if p2 gets there in less time
            voronoi -= 1

    # print(voronoi)
    if player == 0:
        return voronoi  # value for p1
    else:
        return -voronoi  # value for p2


def calc_distances(state):
    # calculates distances from each player to each square, to be used in voronoi function
    locs = state.player_locs
    board = np.array(state.board)
    # ignored player to move, we don't need

    players = np.arange(len(locs))
    players_distance = []

    for player in players:

        # matrix where each cell is distance from player. -1 if can't get there
        distance_matrix = np.negative(np.ones(board.shape))
        distance_matrix[locs[player]] = 0  # isn't locs[player] a tuple? how can you index into distance matrix with a tuple?

        frontier = PriorityQueue()  # What kind of search is this algorithm performing right here
        frontier.put((0, locs[player]))

        while not frontier.empty():
            distance, location = frontier.get()
            adjacent = adjacent_squares(location)
            for square in adjacent:
                if not (board[square] == 'x' or board[square] == '#'):
                    if distance_matrix[square] == -1:
                        distance_matrix[square] = distance + 1
                        frontier.put((distance + 1, square))

        players_distance.append(distance_matrix.flatten())

    return players_distance


def adjacent_squares( location):
    # Returns tuples of squares adjacent to current square
    i = location[0]
    j = location[1]
    return [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
