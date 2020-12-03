def alpha_beta_cutoff(asp, cutoff_ply, eval_func):
    """
    This function should:
    - search through the asp using alpha-beta pruning
    - cut off the search after cutoff_ply moves have been made.

    Inputs:
            asp - an AdversarialSearchProblem
            cutoff_ply- an Integer that determines when to cutoff the search
                    and use eval_func.
                    For example, when cutoff_ply = 1, use eval_func to evaluate
                    states that result from your first move. When cutoff_ply = 2, use
                    eval_func to evaluate states that result from your opponent's
                    first move. When cutoff_ply = 3 use eval_func to evaluate the
                    states that result from your second move.
                    You may assume that cutoff_ply > 0.
            eval_func - a function that takes in a GameState and outputs
                    a real number indicating how good that state is for the
                    player who is using alpha_beta_cutoff to choose their action.
                    You do not need to implement this function, as it should be provided by
                    whomever is calling alpha_beta_cutoff, however you are welcome to write
                    evaluation functions to test your implementation. The eval_func we provide
        does not handle terminal states, so evaluate terminal states the
        same way you evaluated them in the previous algorithms.

    Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
    """

    # initializing variables
    start_state = asp.get_start_state()
    player = start_state.player_to_move()
    optimal_move = None
    alpha = float("-inf")  # note - alpha at the initial state is the same as the max score
    beta = float("inf")

    # finding the best move
    for action in asp.get_available_actions(start_state):
        next_state = asp.transition(start_state, action)
        next_score = cutoff_ab_min_value(asp, next_state, player, alpha, beta, cutoff_ply - 1, eval_func)

        if next_score > alpha:  # if a value is found above the lower bound we increase alpha
            alpha = next_score
            optimal_move = action

    return optimal_move


def cutoff_ab_max_value(asp, state, player, alpha, beta, depth, eval_func):
    """helper function for minimax

    Inputs: asp - an adversarial search problem
           state - the current game state
           player - the player whose turn it is

    Outputs: a value reflecting the minimum possible score that the player can
              attain from a state assuming optimal game play by both players
    """
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    elif depth == 0:
        return eval_func(state)
    else:
        max_score = float("-inf")
        for action in asp.get_available_actions(state):
            next_state = asp.transition(state, action)
            next_score = cutoff_ab_min_value(asp, next_state, player, alpha, beta, depth - 1, eval_func)
            if next_score >= beta:  # if a value is found above the upper bound we prune
                return next_score
            if next_score > alpha:  # if a value is found above the lower bound we increase alpha
                alpha = next_score
            if next_score > max_score:
                max_score = next_score

        return max_score


def cutoff_ab_min_value(asp, state, player, alpha, beta, depth, eval_func):
    """Inputs: asp - an adversarial search problem
           state - the current game state
           player - the player whose turn it is

    Outputs: a value reflecting the maximum possible score that the player can
              attain from a state assuming optimal game play by both players
    """
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    elif depth == 0:
        return eval_func(state)
    else:
        min_score = float("inf")
        for action in asp.get_available_actions(state):
            next_state = asp.transition(state, action)
            next_score = cutoff_ab_max_value(asp, next_state, player, alpha, beta, depth - 1, eval_func)
            if next_score <= alpha:  # if a value is found below the lower bound we prune
                return next_score
            if next_score < beta:  # if a value is found below the upper bound we decrease beta
                beta = next_score
            if next_score < min_score:
                min_score = next_score

        return min_score
