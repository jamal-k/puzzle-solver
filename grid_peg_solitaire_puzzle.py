from puzzle import Puzzle
from copy import deepcopy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> grid3 = [["#", "*", "*", "*", "#"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["#", "*", "*", "*", "#"]]
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gpsp1 == gpsp2
        True
        >>> gpsp1 == gpsp3
        False
        """
        return (type(self) == type(other) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a string representation of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid1 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> print(gpsp1)
        <BLANKLINE>
        *****
        *****
        *****
        **.**
        *****
        <BLANKLINE>
        """
        # string accumulator
        result = "\n"

        # add each list from self._marker as a line to result
        for line in self._marker:
            for marker in line:
                result += marker
            result += '\n'

        return result

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        Overrides Puzzle.extensions

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid1 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> L1 = gpsp1.extensions()
        >>> grid2 = [["*", "*", ".", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> grid3 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", ".", "."], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> grid4 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    [".", ".", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp4 = GridPegSolitairePuzzle(grid4, {"*", ".", "#"})
        >>> grid5 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", ".", "*", "*"]]
        >>> gpsp5 = GridPegSolitairePuzzle(grid5, {"*", ".", "#"})
        >>> L2 = [gpsp2, gpsp3, gpsp4, gpsp5]
        >>> len(L1) == len(L2)
        True
        >>> all([x in L2 for x in L1])
        True
        >>> all([x in L1 for x in L2])
        True
        """
        # list accumulator for all extensions
        lst = []

        # look for two adjacent pegs next to every hole, such that one peg can
        # jump over the other into the hole, then create a new grid to
        # represent each of those jumps, and add to lst

        for row in range(len(self._marker)):
            for column in range(len(self._marker[row])):
                if self._marker[row][column] == '*':
                    # jump to the left if possible
                    if (column - 2) in range(len(self._marker[row])) and \
                            self._marker[row][column - 2] == '.' and \
                            self._marker[row][column - 1] == '*':
                        new_grid = deepcopy(self._marker)
                        new_grid[row] = new_grid[row][:column - 2] + \
                            ["*", ".", "."] + new_grid[row][column + 1:]
                        lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                                                                     "#"}))
                    # jump to the right if possible
                    if (column + 2) in range(len(self._marker[row])) and \
                            self._marker[row][column + 2] == '.' and \
                            self._marker[row][column + 1] == '*':
                        new_grid = deepcopy(self._marker)
                        new_grid[row] = new_grid[row][:column] + \
                            [".", ".", "*"] + new_grid[row][column + 3:]
                        lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                                                                     "#"}))

                    # jump up if possible
                    if (row - 2) in range(len(self._marker)) and \
                            self._marker[row - 2][column] == '.' and \
                            self._marker[row - 1][column] == '*':
                        new_grid = deepcopy(self._marker)
                        new_grid[row - 2][column] = "*"
                        new_grid[row - 1][column] = "."
                        new_grid[row][column] = "."
                        lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                                                                     "#"}))

                    # jump down if possible
                    if (row + 2) in range(len(self._marker)) and \
                            self._marker[row + 2][column] == '.' and \
                            self._marker[row + 1][column] == '*':
                        new_grid = deepcopy(self._marker)
                        new_grid[row + 2][column] = "*"
                        new_grid[row + 1][column] = "."
                        new_grid[row][column] = "."
                        lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                                                                     "#"}))
                # if self._marker[row][column] == '.':
                #     # two pegs to the left of hole
                #     if (column - 2) in range(len(self._marker[row])) and \
                #             self._marker[row][column - 2] == '*' and \
                #             self._marker[row][column - 1] == '*':
                #         new_grid = deepcopy(self._marker)
                #         new_grid[row] = new_grid[row][:column - 2] + \
                #             [".", ".", "*"] + new_grid[row][column + 1:]
                #         lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                #                                                      "#"}))
                #     # two pegs to the right of hole
                #     if (column + 2) in range(len(self._marker[row])) and \
                #             self._marker[row][column + 2] == '*' and \
                #             self._marker[row][column + 1] == '*':
                #         new_grid = deepcopy(self._marker)
                #         new_grid[row] = new_grid[row][:column] + \
                #             ["*", ".", "."] + new_grid[row][column + 3:]
                #         lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                #                                                      "#"}))
                #     # two pegs above hole
                #     if (row - 2) in range(len(self._marker)) and \
                #             self._marker[row - 2][column] == '*' and \
                #             self._marker[row - 1][column] == '*':
                #         new_grid = deepcopy(self._marker)
                #         new_grid[row - 2] = \
                #             new_grid[row - 2][:column] + \
                #             ["."] + new_grid[row - 2][column + 1:]
                #         new_grid[row - 1] = \
                #             new_grid[row - 1][:column] + \
                #             ["."] + new_grid[row - 1][column + 1:]
                #         new_grid[row] = \
                #             new_grid[row][:column] + \
                #             ["*"] + new_grid[row][column + 1:]
                #         lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                #                                                      "#"}))
                #     # two pegs below hole
                #     if (row + 2) in range(len(self._marker)) and \
                #             self._marker[row + 2][column] == '*' and \
                #             self._marker[row + 1][column] == '*':
                #         new_grid = deepcopy(self._marker)
                #         new_grid[row + 2] = \
                #             new_grid[row + 2][:column] + \
                #             ["."] + new_grid[row + 2][column + 1:]
                #         new_grid[row + 1] = \
                #             new_grid[row + 1][:column] + \
                #             ["."] + new_grid[row + 1][column + 1:]
                #         new_grid[row] = \
                #             new_grid[row][:column] + \
                #             ["*"] + new_grid[row][column + 1:]
                #         lst.append(GridPegSolitairePuzzle(new_grid, {"*", ".",
                #                                                      "#"}))

        return lst

    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        Overrides Puzzle.is_solved

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = [["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", "*", "*", "*"], \
                    ["*", "*", ".", "*", "*"], \
                    ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> gpsp1.is_solved()
        False
        >>> grid2 = [[".", ".", ".", ".", "."], \
                    [".", ".", ".", ".", "."], \
                    [".", ".", "*", ".", "."], \
                    [".", ".", ".", ".", "."], \
                    [".", ".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.is_solved()
        True
        """
        # accumulator to count number of pegs
        pegs = 0

        for row in self._marker:
            for marker in row:
                if marker == '*':
                    pegs += 1

        # only solved when one peg remaining
        return pegs == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
