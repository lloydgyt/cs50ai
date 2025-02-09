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
    Biconditional(AKnight, Sentence0A),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Sentence1A = And(AKnave, BKnave)
knowledge1 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    # Every sentence spoken by a knight is true, 
    # and every sentence spoken by a knave is false.

    # A
    Biconditional(AKnight, Sentence1A),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Sentence2A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Sentence2B = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    # A
    Biconditional(AKnight, Sentence2A),
    # B
    Biconditional(BKnight, Sentence2B),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Sentence3A1 = AKnave
Sentence3A2 = AKnight
Sentence3B1 = Biconditional(AKnight, AKnave)
Sentence3B2 = CKnave
Sentence3C = AKnight
knowledge3 = And(
    # one can only be a knight or a knave
    Only_one_identity,
    # A (one of them)
    Or(
        Biconditional(AKnight, Sentence3A1),
        Biconditional(AKnight, Sentence3A2)
    ),
    Not(And(
        Biconditional(AKnight, Sentence3A1),
        Biconditional(AKnight, Sentence3A2)
    )),
    # B
    Biconditional(BKnight, Sentence3B1),
    Biconditional(BKnight, Sentence3B2),
    # C
    Biconditional(CKnight, Sentence3C)
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
