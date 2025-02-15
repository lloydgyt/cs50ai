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
        assert self.has_arc(x, y)
        for word_x in self.domains[x].copy():
            flag = False
            for word_y in self.domains[y].copy():
                if self.is_satisfied(word_x, word_y, x, y):
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
            arcs = set(itertools.permutations(self.crossword.variables, 2))

        while len(arcs) != 0:
            # pop one out
            x, y = arcs.pop()
            # revise it (may get empty?)
            if not self.has_arc(x, y):
                continue
            if self.revise(x, y):
                # if domain empty, return False
                if len(self.domains[x]) == 0: return False
                # add neighbor
                for n in self.crossword.neighbors(x) - {y}:
                    arcs.add((n, x))

        return True

    def has_arc(self, x, y):
        """ 
        check if there is an arc (binary constraint) between X and Y
        """
        if self.crossword.overlaps[(x, y)] is None:
            return False
        else:
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
            if not self.has_arc(x, y):
                continue
            if not self.is_satisfied(assignment[x], assignment[y], x, y):
                return False
        return True
    

    def is_satisfied(self, word_x, word_y, x, y):
        """ 
        check if word_x (the word for X) conflicts with word_y (the word for Y)
        """
        assert self.has_arc(x, y)
        overlap_x_index, overlap_y_index = self.crossword.overlaps[(x, y)]
        return word_x[overlap_x_index] == word_y[overlap_y_index]


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = list(self.domains[var])
        neighbors = list(self.crossword.neighbors(var))
        unassigned_neighbors = [n for n in neighbors if n not in assignment]
        def num_ruleout(word):
            result = 0
            for neighbor in unassigned_neighbors:
                for word_n in self.domains[neighbor]:
                    if self.is_satisfied(word, word_n, var, neighbor):
                        continue
                    result += 1
            return result
        return sorted(domain, key=num_ruleout)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = self.crossword.variables - set(assignment)
        if len(unassigned_vars) == 0:
            return None
        def num_remaining_value(var):
            return len(self.domains[var])
        return sorted(list(unassigned_vars), key=num_remaining_value)[0]



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
        domain_values = self.order_domain_values(var, assignment)
        assert domain_values is not None
        for value in domain_values:
            assignment[var] = value
            # inference - reduce the domain
            original_domain = self.domains.copy()
            # var's domain contains only "VALUE"
            self.domains[var] = set()
            self.domains[var].add(value)
            # add pairs related to VAR to ARCS
            arcs = set([(n, var) for n in self.crossword.neighbors(var)]) 
            self.ac3(arcs)
            # check if the assignment is still consistent?
            if self.consistent(assignment):
                new_assignment = self.backtrack(assignment)
                if new_assignment is not None:
                    return new_assignment
            else:
                # discard this value
                del assignment[var]
                # remove inference
                self.domains = original_domain
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
