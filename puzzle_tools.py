"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """

    def _depth_first_solve(puzz, seen=()):
        """
        Return PuzzleNode that's first in a path of PuzzleNodes that lead to
        solution, or None if no solution found.

        @type puzz: Puzzle
        @type seen: tuple(Puzzle)
        @rtype: PuzzleNode | None
        """
        # initialize the current node
        curr_node = PuzzleNode(puzz)

        # ignore previously seen puzzle config
        if puzz in [x.puzzle for x in seen]:
            return

        # if puzzle impossible, ignore it
        elif puzz.fail_fast():
            # update seen
            seen += (curr_node,)
            return

        # if solution found, add the current node to the solution
        elif puzz.is_solved():
            curr_node.in_solution = True
            return curr_node

        else:
            # update seen
            seen += (curr_node,)
            # make a recursive call for each puzzle extension
            # (perform a depth search)
            for p in puzz.extensions():
                # initialize the new node
                new_node = _depth_first_solve(p, seen=seen)
                # if solution found, add it to the children of the current node,
                # and exit the loop early since there's no need to continue
                # looking for additional solutions
                if new_node and new_node.in_solution:
                    curr_node.children.append(new_node)
                    break

            for p in curr_node.children:
                # if curr_node has a child ...
                if p and p.in_solution:
                    # ... assign curr_node's child's parent to be curr_node
                    p.parent = curr_node
                    # add curr_node to the solution
                    curr_node.in_solution = True

            # return the current node if it's a solution, or None if the puzzle
            # couldn't be solved
            return curr_node if curr_node.in_solution else None

    # use _depth_first_solve on puzzle to find first node of solution
    return _depth_first_solve(puzzle)

def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    def _breadth_first_solve(puzz):
        """
        Return PuzzleNode that's first in a path of PuzzleNodes that lead to
        solution, or None if no solution found.

        @type puzz: Puzzle
        @rtype: PuzzleNode | None
        """
        # initialize tuple of already seen puzzle configs
        seen = ()

        # initialize deque of puzzle nodes to evaluate for solution
        q = deque()

        # assign current node, and add it to queue
        curr_node = PuzzleNode(puzz)
        q.append(curr_node)

        # keep checking next node until solution found or the queue is empty
        while not curr_node.puzzle.is_solved() and len(q) > 0:
            curr_node = q.popleft()
            seen += (curr_node.puzzle,)

            for p in curr_node.puzzle.extensions():
                # don't bother with already seen puzzles
                if p not in seen:
                    new_node = PuzzleNode(p)
                    # form parent relationship
                    new_node.parent = curr_node
                    # add extensions from next level to back of queue
                    q.append(new_node)
                    seen += (new_node.puzzle,)

        # if final node removed from q was the solution, then create a chain of
        # nodes using the parent relationship, and assigning the children
        if curr_node.puzzle.is_solved():
            # keep assigning children up until the root (top node), then return
            # it
            while curr_node.parent:
                curr_node.parent.children.append(curr_node)
                curr_node = curr_node.parent
            return curr_node

        # must have been the case that no solution was found otherwise, so
        # return None
        else:
            return None

    return _breadth_first_solve(puzzle)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None,
                 in_solution=False):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @type in_solution: bool
        @rtype: None
        """
        # self.in_solution is whether or not depth first solver found
        # self to be part of its solution
        self.puzzle, self.parent, self.in_solution = puzzle, parent, in_solution
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
