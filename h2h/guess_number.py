"""
A server holds a secret integer between 1 and upperBound, inclusive. You are given upperBound and a GuessServer, but you cannot read the secret directly. Submit an integer guess by calling String check(int guess).

Feedback is delayed by one call. The first call returns "PENDING". Every later call returns feedback about the previous guess:

"TOO_LOW" if that guess was less than the secret.
"TOO_HIGH" if that guess was greater than the secret.
"CORRECT" if that guess matched the secret.
The guess submitted in the current call becomes the new pending guess.

Implement findNumber(int upperBound, GuessServer server) to return the secret. Every submitted guess must be within the allowed range and distinct from all earlier guesses.

You may return a value as soon as the available information uniquely identifies it, even if the latest pending guess has not received feedback. You should use as few check() calls as possible.

Constraints:

1 ≤ upperBound ≤ 109.
Example 1:

Input: upperBound = 10, secret = 6 (hidden from findNumber)
Output: 6
Explanation: One valid sequence submits 5, 8, 6, and 7: The first response is "PENDING"; The second says 5 was too low, the third says 8 was too high, and the fourth confirms 6 was correct. The response to the fourth call does not describe the newly submitted guess (7).

Example 2:

Input: upperBound = 50, secret = 17 (hidden from findNumber)
Output: 17

Example 3:

Input: upperBound = 31, secret = 25 (hidden from findNumber)
Output: 25

hints:
Maintain a separate variable for your last submitted guess, since its result will only arrive when you make your next API call.
When computing the next midpoint, verify it does not equal the pending guess; if it collides, shift your split point toward the larger half of the remaining interval.
"""
class GuessServer:
    """
    External API that handles the target number and provides feedback on guesses.
    You should NOT directly access the target number.
    """

    def __init__(self, secret, upperBound):
        if secret < 1 or secret > upperBound:
            raise AssertionError("Secret is outside the allowed range")
        self.secret = secret
        self.upperBound = upperBound
        self.submitted = set()
        self.hasPending = False
        self.pendingGuess = 0
        self.callCount = 0

    def check(self, guess):
        if guess < 1 or guess > self.upperBound or guess in self.submitted:
            raise AssertionError("Invalid or repeated guess: " + str(guess))
        self.submitted.add(guess)

        self.callCount += 1
        response = "PENDING"

        if self.hasPending:
            if self.pendingGuess < self.secret:
                response = "TOO_LOW"
            elif self.pendingGuess > self.secret:
                response = "TOO_HIGH"
            else:
                response = "CORRECT"

        self.pendingGuess = guess
        self.hasPending = True
        return response

    def getCallCount(self):
        return self.callCount


class Solution:
    def findNumber(self, upperBound, server):
        # TODO: Implement findNumber logic.
        pass


def test1():
    print("===== Test 1 =====")
    server = GuessServer(6, 10)
    result = Solution().findNumber(10, server)
    print(result)  # Expected: 6
    print("Calls: " + str(server.getCallCount()))


def test2():
    print("===== Test 2 =====")
    server = GuessServer(17, 50)
    result = Solution().findNumber(50, server)
    print(result)  # Expected: 17
    print("Calls: " + str(server.getCallCount()))


def test3():
    print("===== Test 3 =====")
    server = GuessServer(25, 31)
    result = Solution().findNumber(31, server)
    print(result)  # Expected: 25
    print("Calls: " + str(server.getCallCount()))


def test4():
    print("===== Test 4 =====")
    server = GuessServer(1, 100)
    result = Solution().findNumber(100, server)
    print(result)  # Expected: 1
    print("Calls: " + str(server.getCallCount()))


def test5():
    print("===== Test 5 =====")
    server = GuessServer(5, 5)
    result = Solution().findNumber(5, server)
    print(result)  # Expected: 5
    print("Calls: " + str(server.getCallCount()))


def test6():
    print("===== Test 6 =====")
    server = GuessServer(1, 1)
    result = Solution().findNumber(1, server)
    print(result)  # Expected: 1
    print("Calls: " + str(server.getCallCount()))


def test7():
    print("===== Test 7 =====")
    server = GuessServer(1_000_000_000, 1_000_000_000)
    result = Solution().findNumber(1_000_000_000, server)
    print(result)  # Expected: 1000000000
    print("Calls: " + str(server.getCallCount()))


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()