from termcolor import cprint
import minesweeper as ms
from minesweeper import Minesweeper, MinesweeperAI

# DEBUG
def print_knowledge(knowledge):
    """ print each sentence in self.knowledge"""
    for s in knowledge:
        print(f"DEBUG: sentence = {s}")
    
def test_addknowledge4():
    """MinesweeperAI.add_knowledge ignores known mines when adding new sentence"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((0, 0), 3)

    print_knowledge(ai.knowledge)

    ai.mines.update({(0, 1), (1, 0), (1, 1)}) # just in case submission doesn't infer already
    ai.add_knowledge((0, 2), 3)

    print_knowledge(ai.knowledge)

    s = ms.Sentence({(0, 3), (1, 2), (1, 3)}, 1)
    if s not in ai.knowledge:
        raise Exception(f"did not find sentence {s}")

def test_addknowledge9():
    """MinesweeperAI.add_knowledge can infer safe cells when given new information"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((0, 1), 1)
    print_knowledge(ai.knowledge)
    ai.add_knowledge((1, 0), 1)
    print_knowledge(ai.knowledge)
    ai.add_knowledge((1, 2), 1)
    print_knowledge(ai.knowledge)
    ai.add_knowledge((3, 1), 0)
    print_knowledge(ai.knowledge)
    ai.add_knowledge((0, 4), 0)
    print_knowledge(ai.knowledge)
    ai.add_knowledge((3, 4), 0)
    print_knowledge(ai.knowledge)
    safes = [(0, 0), (0, 2)]
    for safe in safes:
        if safe not in ai.safes:
            raise Exception(f"did not find {safe} in safe cells when possible to conclude safe")

# test_addknowledge4()
# test_addknowledge9()

# test game
HEIGHT = 3
WIDTH = 3
MINES = 3

game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

lost = False

while not lost:
    # make an ai move
    move = ai.make_safe_move()
    if move is None:
        move = ai.make_random_move()
        if move is None:
            print("No moves left to make.")
            break
        else:
            print("No known safe moves, AI making random move.")
    else:
        print("AI making safe move.")
    
    # move and update knowledge
    print(f"move = {move}")
    if game.is_mine(move):
        lost = True
    else:
        nearby = game.nearby_mines(move)
        ai.add_knowledge(move, nearby)

if lost == True:
    cprint("You lose.", "red")
elif len(ai.mines) == MINES:
    cprint("You win", "green")
else:
    print("Ended abnormally.")