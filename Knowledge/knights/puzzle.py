from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")



# one can only be a knight or a knave
Only_one_identity = And(
    # one can only be a knight or a knave
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    Or(CKnave, CKnight),
    Not(And(CKnave, CKnight)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
Sentence0A = And(AKnight, AKnave)
knowledge0 = And(
    # has nothing to do with B, so if you don't put anything
    # related to B here, it will not entail!
    # don't think about how model checking happens
    # just try your best to translate

    # one can only be a knight or a knave
    Only_one_identity,

    # Every sentence spoken by a knight is true, 
    # and every sentence spoken by a knave is false.
    Or(And(Sentence0A, AKnight), And(Not(Sentence0A), AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Sentence1A = And(AKnave, BKnave)
# Sentence1B = Nothing
knowledge1 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    # Every sentence spoken by a knight is true, 
    # and every sentence spoken by a knave is false.
    Or(And(Sentence1A, AKnight), And(Not(Sentence1A), AKnave)),
    Or(BKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Sentence2A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Sentence2B = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    Or(And(Sentence2A, AKnight), And(Not(Sentence2A), AKnave)),
    Or(And(Sentence2B, BKnight), And(Not(Sentence2B), BKnave)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Sentence3A = AKnave
Sentence3A2 = AKnight
B_A_said = Or(And(AKnave, AKnight), And(Not(AKnave), AKnave))
Sentence3B = CKnave # and A said??
Sentence3C = AKnight
knowledge3 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    
    # what does 'X said' mean?
    # A
    Or(
        Or(And(Sentence3A, AKnight), And(Not(Sentence3A), AKnave)),
        Or(And(Sentence3A2, AKnight), And(Not(Sentence3A2), AKnave)),
    ),
    # B
    Or(And(Sentence3B, B_A_said, BKnight), And(Not(Sentence3B), Not(B_A_said), BKnave)),
    # C
    Or(And(Sentence3C, CKnight), And(Not(Sentence3C), CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
