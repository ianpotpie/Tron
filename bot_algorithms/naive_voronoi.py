import numpy as np

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def naive_voronoi(state):

    player_scores = np.zeros(2)
    p0_coord = state.player_locs[0]
    p1_coord = state.player_locs[1]

    for row_index, row in enumerate(state.board):
        for col_index, cell in enumerate(row):
            if cell == ' ':
                p0_dist = manhattan_distance(col_index, row_index, p0_coord[1],p0_coord[0])
                p1_dist = manhattan_distance(col_index, row_index, p1_coord[1],p1_coord[0])
                if p0_dist < p1_dist:
                    player_scores[0] += 1
                    player_scores[1] -= 1
                elif p1_dist < p0_dist:
                    player_scores[1] += 1
                    player_scores[0] -= 1

    return player_scores
