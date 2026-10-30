"""
Follow-up:
Extend the previous question to multiple independent games running in parallel.

You are given an integer array upperBounds, where game i has its own hidden secret in [1, upperBounds[i]]. Instead of submitting one guess at a time, submit one guess for every unfinished game using String[] checkBatch(int[] guesses).

Each guesses array must have the same length as upperBounds. For each index i:

While game i is unfinished, guesses[i] must be a new integer in [1, upperBounds[i]]. You cannot skip an unfinished game.
Guess uniqueness is tracked per game. Different games may submit the same integer.
Once game i is resolved, you must submit -1 for guesses[i] in every later batch. -1 does not count as a guess.
As in the previous question, feedback is delayed by one call. checkBatch() returns a string list of feedback, where each feedback describes the guess submitted for game i in the previous batch. feedback[i] is "PENDING" when no previous guess exists for that game, including when the previous batch used -1 at index i.

Every value other than -1 in the current batch counts as an individual guess, even if the returned feedback from the previous batch is enough to determine that game's secret.

Implement int[] findNumbers(int[] upperBounds, BatchGuessServer server) and return the hidden secrets in game-index order.

You may stop submitting guesses for a game as soon as its secret is uniquely determined, and you may return once all games are resolved without requesting feedback for the final pending batch. You should use as few checkBatch() calls as possible.

Constraints:

1 ≤ upperBounds.length ≤ 1000.
1 ≤ upperBounds[i] ≤ 109.
Example 1:

Input: upperBounds = [4, 3], secrets = [3, 1] (hidden from findNumbers)
Output: [3, 1]
Explanation: One possible sequence submission is:

checkBatch([2, 2]) returns ["PENDING", "PENDING"] because there is no preceding batch.
Next, checkBatch([3, 1]) returns ["TOO_LOW", "TOO_HIGH"] for [2, 2], showing that game 0's secret is greater than 2 and game 1's secret is 1.
Finally, checkBatch([4, -1]) returns ["CORRECT", "CORRECT"] for [3, 1], confirming game 0's secret is 3.
The -1 skips the already completed game 1, so no feedback for [4, -1] is needed. The second "CORRECT" is irrelevant because game 1 had already been resolved.
Example 2:

Input: upperBounds = [10, 50, 8], secrets = [6, 17, 4] (hidden from findNumbers)
Output: [6, 17, 4]

Example 3:

Input: upperBounds = [20, 20, 20, 20], secrets = [2, 13, 8, 17] (hidden from findNumbers)
Output: [2, 13, 8, 17]

hint
Maintain separate state for each game's valid range and its most recent submitted guess, remembering that feedback always lags exactly one step behind your submissions.
When building a batch, avoid re-submitting the same midpoint as your pending guess; shift your next query slightly within the narrowed range to prevent wasted turns waiting for delayed results.

"""

class BatchGuessServer:
    """
    External API that holds the secret for each game and returns delayed feedback.
    You should NOT directly access the secret numbers.
    """

    def __init__(self, secrets, upperBounds):
        if len(secrets) != len(upperBounds):
            raise AssertionError("Each game needs a secret and an upper bound")

        self.secrets = list(secrets)
        self.upperBounds = list(upperBounds)
        self.submitted = [set() for _ in secrets]
        self.inactive = [False] * len(secrets)
        self.pending = None
        self.guessCount = 0

        for i in range(len(secrets)):
            if secrets[i] < 1 or secrets[i] > upperBounds[i]:
                raise AssertionError(f"Secret is outside the game range: {i}")

    def checkBatch(self, guesses):
        if len(guesses) != len(self.secrets):
            raise AssertionError("Every batch must include every game")

        feedback = ["PENDING"] * len(self.secrets)

        if self.pending is not None:
            for i in range(len(self.secrets)):
                if self.pending[i] == -1:
                    continue

                if self.pending[i] < self.secrets[i]:
                    feedback[i] = "TOO_LOW"
                elif self.pending[i] > self.secrets[i]:
                    feedback[i] = "TOO_HIGH"
                else:
                    feedback[i] = "CORRECT"

        for i in range(len(guesses)):
            if guesses[i] == -1:
                self.inactive[i] = True
                continue

            if (self.inactive[i] or guesses[i] < 1 or guesses[i] > self.upperBounds[i]
                    or guesses[i] in self.submitted[i]):
                raise AssertionError(f"Invalid or repeated guess for game {i}")
            self.submitted[i].add(guesses[i])

            self.guessCount += 1

        self.pending = list(guesses)
        return feedback

    def getGuessCount(self):
        return self.guessCount


class Solution:
    def findNumbers(self, upperBounds, server):
        # TODO: Implement findNumbers logic.
        pass


def test1():
    print("===== Test 1 =====")

    upperBounds = [4, 3]
    server = BatchGuessServer([3, 1], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [3, 1]
    print(f"Total guesses: {server.getGuessCount()}")


def test2():
    print("===== Test 2 =====")

    upperBounds = [10, 50, 8]
    server = BatchGuessServer([6, 17, 4], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [6, 17, 4]
    print(f"Total guesses: {server.getGuessCount()}")


def test3():
    print("===== Test 3 =====")

    upperBounds = [20, 20, 20, 20]
    server = BatchGuessServer([2, 13, 8, 17], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [2, 13, 8, 17]
    print(f"Total guesses: {server.getGuessCount()}")


def test4():
    print("===== Test 4 =====")

    upperBounds = [4, 50]
    server = BatchGuessServer([3, 29], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [3, 29]
    print(f"Total guesses: {server.getGuessCount()}")


def test5():
    print("===== Test 5 =====")

    upperBounds = [5, 5, 5]
    server = BatchGuessServer([1, 3, 5], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [1, 3, 5]
    print(f"Total guesses: {server.getGuessCount()}")


def test6():
    print("===== Test 6 =====")

    upperBounds = [1, 1, 1]
    server = BatchGuessServer([1, 1, 1], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [1, 1, 1]
    print(f"Total guesses: {server.getGuessCount()}")


def test7():
    print("===== Test 7 =====")

    upperBounds = [1_000_000_000, 1_000_000_000, 1]
    server = BatchGuessServer([1_000_000_000, 1, 1], upperBounds)
    result = Solution().findNumbers(upperBounds, server)
    print(result)  # Expected: [1000000000, 1, 1]
    print(f"Total guesses: {server.getGuessCount()}")


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()