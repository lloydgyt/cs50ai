import sys

from crossword import *
from generate import *

def test_enforce_node_consistency():

    # Check usage
    # if len(sys.argv) not in [3, 4]:
    #     sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    output = None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    
    print(f"DEBUG: original domain:")
    for v in creator.crossword.variables:
        print(creator.domains[v])
        print()

    creator.enforce_node_consistency()

    print(f"DEBUG: current domain:")
    for v in creator.crossword.variables:
        print(creator.domains[v])
        print()
    # assignment = creator.solve()

    # Print result
    # if assignment is None:
    #     print("No solution.")
    # else:
    #     creator.print(assignment)
    #     if output:
    #         creator.save(assignment, output)

def test_assignment_complete1():
    """assignment_complete identifies incomplete assignment"""

    # Setup
    Var = Variable
    crossword = Crossword("data/test_structure1.txt", "data/test_words4.txt")
    creator = CrosswordCreator(crossword)

    # Action
    assignment = {
        Var(0, 1, "across", 5): "WHERE",
        Var(2, 1, "across", 5): "SLOPE",
        Var(2, 4, "down", 3): "PAN",
        Var(4, 1, "across", 5): "PAINT"
    }

    result = creator.assignment_complete(assignment)
    expected = False
    assert expected == result

# test_enforce_node_consistency()
