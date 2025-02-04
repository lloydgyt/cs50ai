"""
Tic Tac Toe Player
"""

import math
import copy
from ucb import trace

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

# def max_value(board):
#     """
#     return the value of the given BOARD under using max strategy
#     """
#     if terminal(board):
#         return utility(board)
#     else:
#         value = -1 # set a smallest value at first
#         valid_actions = actions(board)
#         for action in valid_actions:
#             next_value = min_value(result(board, action))
#             value = value if value > next_value else next_value
#         return value


# def min_value(board):
#     """
#     return the value of the given BOARD under using min strategy
#     """
#     if terminal(board):
#         return utility(board)
#     else:
#         value = 1 # set a smallest value at first
#         valid_actions = actions(board)
#         for action in valid_actions:
#             next_value = max_value(result(board, action))
#         # TODO maybe a little pruning is helpful
#             value = value if value < next_value else next_value
#         return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def value_and_action(board):
        """
        calculate the value of BOARD by simulating entire games
        return the value of BOARD, and the optimal_action to get that value
        """
        # TODO its purpose should not be limited at returning a value
        # this fn derives the actions too, which is also useful! 
        # return the value of the given BOARD
        if terminal(board):
            return utility(board), None
        else:
            whos_turn = player(board)
            valid_actions = actions(board)
            # TODO maybe a little pruning is helpful

            if whos_turn == X:
                value_and_action_pair = [value_and_action(result(board, action)) for action in valid_actions]
                return max()
            else:
                return min([value_and_action(result(board, action)) for action in valid_actions])
    whos_turn = player(board)
    valid_actions = actions(board)
    # function to calculate possible values
    # FIXME what if valid_action is []
    assert valid_actions is not None
    possible_boards = [result(board, action) for action in valid_actions]

    # FIXME don't repeat yourself?
    if whos_turn == X:
        # get all states and then calculate value, or get states and then calc values
        # TODO this is where pruning can happen?
        return max([possible_boards], key=min_value)
    elif whos_turn == O:
        return min([possible_boards], key=max_value)
    else: # the game has terminated
        return None

    # max player will want to maxmize the value of the board
    # min player will want to minimize the value of the board
    # (how to choose depend on the player)
    # terminal state has utility, 