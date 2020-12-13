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


def calculate_player_square_distances(state):
    """This function takes a state as input and calculates the distances between each player and each location"""

    player_locations = state.player_locs  # Storing the locations of players. # is this line necessary?
    np_board = np.array(state.board)  # Storing the board as a numpy array so that we can operate on it
    players = np.arange(len(player_locations))  # There are just two players indexed as such

    output = []  # Will eventually contain the distances

    for player in players:

        distances = np.ones(np_board.shape)  # This will represent the board as a grid, with each celling representing the distance
        distances.fill(float('inf'))  # This line sets all the distances initially to be infinity
        distances[player_locations[player]] = 0  # Player is 0 units away from their start location

        pq = PriorityQueue()  # This priority queue will contain locations
        pq.put((0, player_locations[player]))  # The first item in the priority queue is the start location; priority (equivalently, distance) = 0

        while not pq.empty():
            distance, location = pq.get()  # popping from the pq

            # We need to find the adjacent squares in this step in order to calculate distances
            x_pos = location[0]
            y_pos = location[1]
            adjacent_squares = [(x_pos + 1, y_pos), (x_pos-1, y_pos), (x_pos, y_pos+1), (x_pos, y_pos-1)]

            # Now, we loop through the adjacent squares
            for square in adjacent_squares:
                if not (np_board[square] == '#' or np_board[square] == 'x'):  # If the spot on the board is not a wall or permanent wall
                    if distances[square] == float('inf') or distances[square] > distance+1:  # If the square is hitherto unreached
                        pq.put((distance + 1, square))  # We add it to the pq
                        distances[square] = distance + 1  # We mark it as being one step farther from the player than current square
        output.append(distances.flatten())  # Building output

    return output


def arjun_voronoi(state, player):
    distance_holder = calculate_player_square_distances(state)

    difference_in_distances = distance_holder[0] - distance_holder[1]  # A negative value for the above -> p1 is closer. positive -> p2 is closer.
    size = len(difference_in_distances)

    accumulator = 0  # This is where we actually calculate "voronoi"
    for k in range(size):
        # There are four possibilities
        if (distance_holder[0])[k] >= 0 and distance_holder[1][k] == float('inf'):  # Accessible to 1; not 2
            accumulator = accumulator + 1
        elif (distance_holder[0])[k] == float('inf') and distance_holder[1][k] >= 0:
            accumulator = accumulator - 1
        elif difference_in_distances[k] < 0:
            accumulator = accumulator + 1
        elif difference_in_distances[k] > 0:
            accumulator = accumulator - 1

    if player == 0:
        return accumulator
    if player == 1:
        return -1 * accumulator
