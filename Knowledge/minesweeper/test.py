import minesweeper as ms

ai = ms.MinesweeperAI(height=3, width=3)
ai.add_knowledge((0, 2), 0)
options = [(0, 1), (1, 1), (1, 2)]
move = ai.make_safe_move()
print(f"DEBUG: move = {move}")
if move not in options:
    raise Exception(f"move made not one of the safe options")