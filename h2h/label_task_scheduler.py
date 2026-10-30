"""
A data labeling platform manages tasks, human annotators, and AI models. Each entity is represented by a 1-indexed string ID.

You are given integers totalTask, totalModel, totalHuman, and k:

Tasks are labeled "t1", "t2", ..., "t{totalTask}".
Models are labeled "m1", "m2", ..., "m{totalModel}".
Human annotators are labeled "h1", "h2", ..., "h{totalHuman}".
An assignment is represented as [task, model, human], meaning the specified human annotates the specified task using the specified model. A task may appear in multiple assignments, meaning the same task can be annotated by multiple humans and paired with multiple models.

Return any valid schedule as a list of assignments such that:

Each human appears in at least k assignments.
The same human cannot annotate the same task more than once.
Every assignment uses valid task, model, and human IDs within the given ranges.
If no valid schedule exists, return an empty list.

Constraints:

1 ≤ totalTask, totalModel, totalHuman ≤ 100
0 ≤ k ≤ totalTask
Example 1:

Input: totalTask = 3, totalModel = 1, totalHuman = 2, k = 2
Output: [["t1", "m1", "h1"], ["t2", "m1", "h2"], ["t2", "m1", "h1"], ["t3", "m1", "h2"]]
Explanation: This is one of the possible answers. Each human annotates 2 distinct tasks: "h1" works on "t1" and "t2", while "h2" works on "t2" and "t3". Neither human annotates the same task twice, and both satisfy the minimum requirement of k = 2 assignments.

Example 2:

Input: totalTask = 1, totalModel = 1, totalHuman = 1, k = 1
Output: [["t1", "m1", "h1"]]

Example 3:

Input: totalTask = 2, totalModel = 3, totalHuman = 3, k = 2
Output: [["t1", "m1", "h1"], ["t2", "m1", "h2"], ["t1", "m1", "h3"], ["t2", "m1", "h1"], ["t1", "m1", "h2"], ["t2", "m1", "h3"]]

Start by identifying the absolute maximum number of unique tasks a single human can handle, which reveals the feasibility condition.
Instead of filling assignments arbitrarily, structure your logic into discrete rounds where every human receives exactly one assignment per round.
Use a simple cyclic shift or modulo operation on the task index for each human to guarantee that no (task, human) pair repeats across rounds.


"""
class Solution:
    def buildSchedule(self, totalTask, totalModel, totalHuman, k):
        # TODO: Implement buildSchedule logic.

    # Helper function to check if the schedule is valid
    def isValidSchedule(self, result, totalTask, totalModel, totalHuman, k):
        if result is None:
            return False

        impossible = k > totalTask
        if k > 0 and (totalTask <= 0 or totalModel <= 0 or totalHuman <= 0):
            impossible = True

        if impossible:
            return len(result) == 0

        humanCount = [0] * (totalHuman + 1)
        seenPair = set()

        for assignment in result:
            if assignment is None or len(assignment) != 3:
                return False

            taskId = self.parseIdInRange(assignment[0], "t", totalTask)
            modelId = self.parseIdInRange(assignment[1], "m", totalModel)
            humanId = self.parseIdInRange(assignment[2], "h", totalHuman)
            if taskId == -1 or modelId == -1 or humanId == -1:
                return False

            pairKey = str(taskId) + "#" + str(humanId)
            if pairKey in seenPair:
                return False
            seenPair.add(pairKey)

            humanCount[humanId] = humanCount[humanId] + 1

        for humanId in range(1, totalHuman + 1):
            if humanCount[humanId] < k:
                return False

        return True

    def parseIdInRange(self, value, prefix, maxValue):
        if value is None or not value.startswith(prefix):
            return -1

        numberPart = value[len(prefix):]
        if len(numberPart) == 0:
            return -1

        if not numberPart.isdigit():
            return -1

        id = int(numberPart)
        if id < 1 or id > maxValue:
            return -1

        return id

def test1():
    print("===== Test 1 =====")
    solution = Solution()
    result = solution.buildSchedule(3, 1, 2, 2)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t2, m1, h2], [t2, m1, h1], [t3, m1, h2]]
    print(solution.isValidSchedule(result, 3, 1, 2, 2))
    # Expected: true

def test2():
    print("===== Test 2 =====")
    solution = Solution()
    result = solution.buildSchedule(1, 1, 1, 1)
    print(result)
    # One of the possible outputs: [[t1, m1, h1]]
    print(solution.isValidSchedule(result, 1, 1, 1, 1))
    # Expected: true

def test3():
    print("===== Test 3 =====")
    solution = Solution()
    result = solution.buildSchedule(2, 3, 3, 2)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t2, m1, h2], [t1, m1, h3], [t2, m1, h1], [t1, m1, h2], [t2, m1, h3]]
    print(solution.isValidSchedule(result, 2, 3, 3, 2))
    # Expected: true

def test4():
    print("===== Test 4 =====")
    solution = Solution()
    result = solution.buildSchedule(4, 2, 2, 4)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t2, m1, h2], [t2, m1, h1], [t3, m1, h2], [t3, m1, h1], [t4, m1, h2], [t4, m1, h1], [t1, m1, h2]]
    print(solution.isValidSchedule(result, 4, 2, 2, 4))
    # Expected: true

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()