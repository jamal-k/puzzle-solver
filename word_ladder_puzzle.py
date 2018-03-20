from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> w1 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w2 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w3 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save", "cars"})
        >>> w1 == w2
        True
        >>> w2 == w3
        False
        """
        return (type(self) == type(other) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set and
                self._chars == other._chars)

    def __str__(self):
        """
        Return a string representation of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w1 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> print(w1)
        cost -> save
        """
        return "{} -> {}".format(self._from_word, self._to_word)

    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        Overrides Puzzle.extensions

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w1 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w1.extensions() == [WordLadderPuzzle("cast", "save", \
                                {"cost", "cast", "case", "cave", "save"})]
        True
        """
        # list accumulator for all extensions
        lst = []

        # check each letter of self._from_word
        for i in range(len(self._from_word)):
            # check each available character for current letter
            for c in self._chars:
                new_word = self._from_word[:i] + c + self._from_word[i + 1:]
                if new_word in self._word_set and new_word != self._from_word:
                    lst.append(WordLadderPuzzle(new_word, self._to_word,
                                                self._word_set))

        return lst

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        Overrides Puzzle.is_solved

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w1 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w2 = WordLadderPuzzle("save", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w1.is_solved()
        False
        >>> w2.is_solved()
        True
        """
        return self._from_word == self._to_word

    def fail_fast(self):
        """
        Return True iff WordLadderPuzzle self can never be extended to a
        solution.

        Overrides Puzzle.fail_fast

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> w1 = WordLadderPuzzle("cost", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w2 = WordLadderPuzzle("sam", "save", \
        {"cost", "cast", "case", "cave", "save"})
        >>> w1.fail_fast()
        False
        >>> w2.fail_fast()
        True
        """
        return len(self._from_word) != len(self._to_word)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words.txt", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
