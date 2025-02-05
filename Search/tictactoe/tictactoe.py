"""
Tic Tac Toe Player
"""

import math
import copy
from ucb import trace
import operator

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# @trace
def player(board):
    """
    Returns player who has the next turn on a board.

    >>> board = initial_state()
    >>> player(board)
    'X'
    >>> board =  [["X", EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]
    >>> player(board)
    'O'
    """

    if terminal(board):
        return None

    # count the num of Xs and Os
    num_X, num_O = 0, 0
    for row in board:
        for cell in row:
            if cell == "X": num_X += 1
            elif cell == "O": num_O += 1
    if num_X == num_O: return X
    else: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return None
    # return the place where the cell is empty
    coordinates = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: coordinates.add((i, j))
    return coordinates


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    >>> board = [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]
    >>> newb = result(board, (0, 0))
    >>> newb
    [['X', None, None], [None, None, None], [None, None, None]]
    >>> result(newb, (0, 1))
    [['X', 'O', None], [None, None, None], [None, None, None]]
    """
    turn = player(board)
    valid_actions = actions(board)
    new_board = copy.deepcopy(board)

    # check action validity
    if action not in valid_actions:
        raise Exception("invalid action")
    # get coordinates
    i, j = action[0], action[1] 

    if turn == X:
        new_board[i][j] = X
    else:
        new_board[i][j] = O
    return new_board
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    who_wins = None
    def check_win_condition(pos1, pos2, pos3):
        # if three are the same, rebind winner, return ture
        nonlocal who_wins
        cell_pos1 = board[pos1[0]][pos1[1]]
        cell_pos2 = board[pos2[0]][pos2[1]]
        cell_pos3 = board[pos3[0]][pos3[1]]
        if not all([cell_pos1, cell_pos2, cell_pos3]):
            return None
        elif cell_pos1 == cell_pos2 == cell_pos3:
            who_wins = cell_pos1
            return True
    check_pos = []
    # add row checking
    for row in range(3):
        check_pos.append(((row, 0), (row, 1), (row, 2)))
    # add col checking
    for col in range(3):
        check_pos.append(((0, col), (1, col), (2, col)))
    # add diagonal checking
    check_pos.append(((0, 0), (1, 1), (2, 2)))
    check_pos.append(((0, 2), (1, 1), (2, 0)))
    for args in check_pos:
        if check_win_condition(*args) == True:
            return who_wins
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.

    >>> board =  [["X", "X", "X"],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]
    >>> terminal(board)
    True
    """
    def has_any_space(board):
        for row in board:
            for cell in row:
                if cell is EMPTY: return True
        return False

    # print(f"DEBUG: winner = {winner(board)}")
    if winner(board) is not None:
        return True
    elif not has_any_space(board): # this is tie
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    assert terminal(board), "the board is not terminated, it has no utility"
    who_wins = winner(board)
    if who_wins == X: return 1
    elif who_wins == O: return -1
    else: return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    >>> board = initial_state()
    >>> board = result(board, (0, 0))
    >>> board = result(board, (1, 1))
    >>> board = result(board, (0, 1))
    >>> minimax(board)
    (0, 2)
    """
    strategy = {"X": {"init_value": -1,
                        "compare_func": operator.gt},
                "O": {"init_value": 1,
                        "compare_func": operator.lt}}
    def value_and_action(board, alpha, beta):
        """
        ALPHA is the best value max player (X) can have currently
        BETA is the best value min player (O) can have currently
        use ALPHA and BETA to determine whether or not to explore
        a branch
        when in X's turn, we calculate BETA to determine ALPHA
        """
        # if the game has terminated
        if terminal(board):
            return utility(board), None

        whos_turn = player(board)
        valid_actions = actions(board)
        value = strategy[whos_turn]["init_value"]
        compare_func = strategy[whos_turn]["compare_func"]
        optimal_action = None

        # simulating games
        for action in valid_actions:
            new_board = result(board, action)
            new_value = value_and_action(new_board, alpha, beta)[0]
            # updating optimal value and action
            if compare_func(new_value, value):
                value, optimal_action = new_value, action
                # update alpha, beta
                if whos_turn == "X":
                    alpha = value
                else:
                    beta = value
            # pruning
            if beta < alpha:
                break
        return value, optimal_action
    return value_and_action(board, -1, 1)[1]

