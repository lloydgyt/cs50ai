import sys
import itertools

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.crossword.variables.copy():
            for word in self.domains[v].copy():
                if len(word) != v.length: self.domains[v].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap_index = self.crossword.overlaps[(x, y)]
        # if not overlap
        if overlap_index == None:
            return revised
        overlap_x, overlap_y = overlap_index
        for word_x in self.domains[x].copy():
            # TODO use any()
            flag = False
            for word_y in self.domains[y].copy():
                # TODO wrap as a function
                if word_x[overlap_x] == word_y[overlap_y]:
                    flag = True
                    break
            if not flag:
                self.domains[x].remove(word_x)
                revised = True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = set() # TODO does set support pop()? why insisted on using Queue?  # TODO refactor using lib tool?
            for x in self.crossword.variables.copy():
                for y in self.crossword.variables.copy():
                    if x != y: arcs.add((x, y))

        while len(arcs) != 0:
            # pop one out
            x, y = arcs.pop()
            # revise it (may get empty?)
            if self.revise(x, y):
                # if domain empty, return False
                if len(self.domains[x]) == 0: return False
                # add neighbor
                for n in self.crossword.neighbors(x) - {y}:
                    arcs.add((n, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        return all([
        self.is_unique(assignment),
        self.is_assignment_nc(assignment),
        self.is_assignment_ac(assignment)
        ])
    
    
    def is_unique(self, assignment):
        words = assignment.values()
        uniq_words = set(words)
        return False if len(words) != len(uniq_words) else True


    def is_assignment_nc(self, assignment):
        for v in assignment.keys():
            if len(assignment[v]) != v.length: return False
        return True


    def is_assignment_ac(self, assignment):
        for x, y in itertools.combinations(assignment, 2):
            if self.is_conflict(assignment[x], assignment[y], x, y):
                return False
        return True
    

    def is_conflict(self, word_x, word_y, x, y):
        """ 
        check if word_x (the word for X) conflicts with word_y (the word for Y)
        """

        overlap_index = self.crossword.overlaps[(x, y)]
        # if not overlap, then not conflict
        if overlap_index == None:
            return False
        overlap_x, overlap_y = overlap_index
        return word_x[overlap_x] != word_y[overlap_y]


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # TODO upgrade this with heuristic
        return self.domains[var].copy()


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # TODO upgrade this using the minimum remaining value heuristic and then the degree heuristic
        unassigned_vars = self.crossword.variables - set(assignment)
        if len(unassigned_vars) == 0:
            return None
        return list(unassigned_vars)[0]



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if current assignment leads to a successful assignment, return it
        # if all the value tried for the selected variable fails,
        # there is no possible solution to current assignment, return None

        # select an unassigned var
        var = self.select_unassigned_variable(assignment)
        # all variable assigned
        if var is None:
            return assignment
        # try all values in its domain, add it to assignment
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            # TODO add inference here
            # check the system is still consistent?
            if self.consistent(assignment):
                new_assignment = self.backtrack(assignment)
                if new_assignment is not None:
                    return new_assignment
            else:
                # discard this value
                del assignment[var]
                # TODO remove inference, too
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
