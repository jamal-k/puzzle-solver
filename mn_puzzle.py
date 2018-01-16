from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle
        @rtype: bool

        >>> mn1 = MNPuzzle((("*", "2", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> mn2 = MNPuzzle((("*", "2", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> mn3 = MNPuzzle((("1", "2", "3"), ("4", "5", "*")), \
            (("*", "2", "3"), ("4", "5", "1")))
        >>> mn1 == mn2
        True
        >>> mn1 == mn3
        False
        """
        return (type(self) == type(other) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid and
                self.m == other.m and
                self.n == other.n)

    def __str__(self):
        """
        Return a string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> mn1 = MNPuzzle((("*", "2", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> print(mn1)
        <BLANKLINE>
         * 2 3
         4 5 1
        <BLANKLINE>
        """
        # string accumulator
        result = "\n"

        for n in self.from_grid:
            for m in n:
                result += " " + m
            result += "\n"

        return result

    # TODO
    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        Overrides Puzzle.extensions

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> mn1 = MNPuzzle((("*", "2", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> L1 = mn1.extensions()
        >>> mn2 = MNPuzzle((("2", "*", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> mn3 = MNPuzzle((("4", "2", "3"), ("*", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> L2 = [mn2, mn3]
        >>> len(L1) == len(L2)
        True
        >>> all([x in L2 for x in L1])
        True
        >>> all([x in L1 for x in L2])
        True
        """
        # list accumulator for all extensions
        lst = []

        for row in range(self.n):
            for column in range(self.m):
                if self.from_grid[row][column] == "*":
                    if row - 1 in range(self.n):
                        # make all tuples in grid lists, for object assignment
                        new_grid = [list(x) for x in self.from_grid]
                        new_grid[row - 1][column] = "*"
                        new_grid[row][column] = self.from_grid[row - 1][column]
                        # change back to tuples, for new from_grid
                        t = ()
                        for n in new_grid:
                            t += (tuple(n),)
                        lst.append(MNPuzzle(t, self.to_grid))

                    if row + 1 in range(self.n):
                        # make all tuples in grid lists, for object assignment
                        new_grid = [list(x) for x in self.from_grid]
                        new_grid[row + 1][column] = "*"
                        new_grid[row][column] = self.from_grid[row + 1][column]
                        # change back to tuples, for new from_grid
                        t = ()
                        for n in new_grid:
                            t += (tuple(n),)
                        lst.append(MNPuzzle(t, self.to_grid))

                    if column - 1 in range(self.m):
                        # make all tuples in grid lists, for object assignment
                        new_grid = [list(x) for x in self.from_grid]
                        new_grid[row][column - 1] = "*"
                        new_grid[row][column] = self.from_grid[row][column - 1]
                        # change back to tuples, for new from_grid
                        t = ()
                        for n in new_grid:
                            t += (tuple(n),)
                        lst.append(MNPuzzle(t, self.to_grid))

                    if column + 1 in range(self.m):
                        # make all tuples in grid lists, for object assignment
                        new_grid = [list(x) for x in self.from_grid]
                        new_grid[row][column + 1] = "*"
                        new_grid[row][column] = self.from_grid[row][column + 1]
                        # change back to tuples, for new from_grid
                        t = ()
                        for n in new_grid:
                            t += (tuple(n),)
                        lst.append(MNPuzzle(t, self.to_grid))
        return lst

    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        Overrides Puzzle.is_solved

        @type self: MNPuzzle
        @rtype: bool

        >>> mn1 = MNPuzzle((("*", "2", "3"), ("4", "5", "1")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> mn2 = MNPuzzle((("1", "2", "3"), ("4", "5", "*")), \
            (("1", "2", "3"), ("4", "5", "*")))
        >>> mn1.is_solved()
        False
        >>> mn2.is_solved()
        True
        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
