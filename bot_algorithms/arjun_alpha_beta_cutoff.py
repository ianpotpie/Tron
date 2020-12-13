import math



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
                    evaluation functions to test your implemention. The eval_func we provide
        does not handle terminal states, so evaluate terminal states the
        same way you evaluated them in the previous algorithms.

    Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
    """
    starting_state = asp.get_start_state()
    current_player = starting_state.player_to_move()
    available_actions = asp.get_available_actions(starting_state)
    optimal_action = None
    maximum_score = -math.inf
    alpha = -math.inf
    beta = math.inf
    for action in asp.get_available_actions(starting_state):
        child_state = asp.transition(starting_state,action)
        score = mini_alpha_beta_cutoff(asp, child_state, eval_func,current_player,alpha,beta,cutoff_ply-1)
        if score > maximum_score:
            optimal_action = action
            maximum_score = score
        if score >= beta:
            return action
        if score > alpha:
            alpha = score
    return optimal_action

def mini_alpha_beta_cutoff(asp, state, eval_func, player,alpha,beta,cutoff):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    if cutoff == 0:
        return eval_func(state)
    else:
        minimum_score = math.inf
        for action in asp.get_available_actions(state):
            child_state = asp.transition(state, action)
            score = maxi_alpha_beta_cutoff(asp, child_state, eval_func,player, alpha, beta,cutoff-1)
            minimum_score=min(minimum_score,score)
            if score <= alpha:
                return score
            if score < beta:
                beta = score
        return minimum_score




def maxi_alpha_beta_cutoff(asp, state, eval_func, player,alpha,beta,cutoff):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    if cutoff == 0:
        return eval_func(state)
    else:
        maximum_score = -math.inf
        for action in asp.get_available_actions(state):

            child_state = asp.transition(state, action)
            score = mini_alpha_beta_cutoff(asp, child_state,eval_func,player,alpha,beta,cutoff-1)
            maximum_score = max(maximum_score,score)
            if score >= beta:
                return score
            if score > alpha:
                alpha = score
        return maximum_score