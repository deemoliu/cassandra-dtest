"""
Follow-up:
In this follow-up, return a schedule that is prefix-balanced.

A prefix is the first x assignments in the schedule for any x >= 1. For example, a schedule with 4 assignments has 4 prefixes: the first assignment, the first 2 assignments, the first 3 assignments, and the full schedule. The balance requirements must hold for every prefix, not only for the final schedule.

A schedule is prefix-balanced if it satisfies both conditions below:

Task-Model Balance: For each task, the number of times it is assigned to each model must differ by at most 1, including models with no uses. Formally, for every task: max_count(task, model) - min_count(task, model) <= 1

A balanced example: task "t1" is assigned with "m1" twice and "m2" once. The difference is 1.
A not-balanced example: task "t1" is assigned with "m1" three times and "m2" zero times. The difference is 3.
Human-Model Balance: For each human, the usage count across all models must differ by at most 1 (including models with 0 uses). Formally: max_count(human, model) - min_count(human, model) <= 1.

A balanced example: human "h1" uses "m1" once and "m2" once. The difference is 0.
A not-balanced example: human "h1" uses "m1" twice and "m2" zero times. The difference is 2.
Return any valid prefix-balanced schedule. If no such schedule exists, return an empty list.

Constraints:

1 ≤ totalTask, totalModel, totalHuman ≤ 10
0 ≤ k ≤ totalTask
Example 1:

Input: totalTask = 3, totalModel = 2, totalHuman = 4, k = 2
Output: [["t1", "m1", "h1"], ["t1", "m2", "h2"], ["t1", "m1", "h3"], ["t1", "m2", "h4"], ["t2", "m2", "h1"], ["t2", "m1", "h2"], ["t2", "m2", "h3"], ["t2", "m1", "h4"]]
Explanation: This is one of the possible answers. Each annotator participates in at least 2 assignments. No annotator labels the same task twice. Across every prefix of the schedule, model usage remains balanced for each task and also for each human.

Example 2:

Input: totalTask = 1, totalModel = 1, totalHuman = 1, k = 1
Output: [["t1", "m1", "h1"]]

Example 3:

Input: totalTask = 3, totalModel = 1, totalHuman = 3, k = 2
Output: [["t1", "m1", "h1"], ["t1", "m1", "h2"], ["t1", "m1", "h3"], ["t2", "m1", "h1"], ["t2", "m1", "h2"], ["t2", "m1", "h3"]]

hint
Track assignment frequencies using frequency maps or arrays, and update them immediately after each candidate placement.
Enforce a deterministic iteration order for tasks and models to reduce branching factor and improve reproducibility.
Implement early termination by validating the balance delta before recursing; if either condition would violate the <=1 difference, backtrack immediately.

"""

class Solution:
    def buildBalancedSchedule(self, totalTask, totalModel, totalHuman, k):
        # TODO: Implement buildBalancedSchedule logic.
        pass

# Helper function to check if the model assignment is balanced
def isBalancedSchedule(result, totalTask, totalModel, totalHuman, k):
    if result is None:
        return False

    impossible = k > totalTask
    if k > 0 and (totalTask <= 0 or totalModel <= 0 or totalHuman <= 0):
        impossible = True

    if impossible:
        return len(result) == 0

    humanCount = [0] * (totalHuman + 1)
    seenPair = set()

    for assign in result:
        if assign is None or len(assign) != 3:
            return False

        taskId = parseIdInRange(assign[0], "t", totalTask)
        modelId = parseIdInRange(assign[1], "m", totalModel)
        humanId = parseIdInRange(assign[2], "h", totalHuman)
        if taskId == -1 or modelId == -1 or humanId == -1:
            return False

        pairKey = str(taskId) + "#" + str(humanId)
        if pairKey in seenPair:
            return False
        seenPair.add(pairKey)

        humanCount[humanId] += 1

    for humanId in range(1, totalHuman + 1):
        if humanCount[humanId] < k:
            return False

    taskModelCount = [[0] * (totalModel + 1) for _ in range(totalTask + 1)]
    humanModelCount = [[0] * (totalModel + 1) for _ in range(totalHuman + 1)]

    for assign in result:
        taskId = parseIdInRange(assign[0], "t", totalTask)
        modelId = parseIdInRange(assign[1], "m", totalModel)
        humanId = parseIdInRange(assign[2], "h", totalHuman)

        taskModelCount[taskId][modelId] += 1
        humanModelCount[humanId][modelId] += 1

        if not isTaskModelBalanced(taskModelCount, taskId, totalModel):
            return False

        if not isHumanModelBalanced(humanModelCount, humanId, totalModel):
            return False

    return True

def isTaskModelBalanced(taskModelCount, taskId, totalModel):
    minCount = float('inf')
    maxCount = float('-inf')

    for modelId in range(1, totalModel + 1):
        minCount = min(minCount, taskModelCount[taskId][modelId])
        maxCount = max(maxCount, taskModelCount[taskId][modelId])

    return maxCount - minCount <= 1

def isHumanModelBalanced(humanModelCount, humanId, totalModel):
    minCount = float('inf')
    maxCount = float('-inf')

    for modelId in range(1, totalModel + 1):
        minCount = min(minCount, humanModelCount[humanId][modelId])
        maxCount = max(maxCount, humanModelCount[humanId][modelId])

    return maxCount - minCount <= 1

def parseIdInRange(value, prefix, maxValue):
    if value is None or not value.startswith(prefix):
        return -1

    numberPart = value[len(prefix):]
    if not numberPart:
        return -1

    if not numberPart.isdigit():
        return -1

    id = int(numberPart)
    if id < 1 or id > maxValue:
        return -1

    return id

def test1():
    print("===== Test 1 =====")
    result = Solution().buildBalancedSchedule(3, 2, 4, 2)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t1, m2, h2], [t2, m1, h3], [t2, m2, h4], [t2, 
    # m2, h1], [t2, m1, h2], [t1, m2, h3], [t1, m1, h4]]
    print(isBalancedSchedule(result, 3, 2, 4, 2))
    # Expected: true

def test2():
    print("===== Test 2 =====")
    result = Solution().buildBalancedSchedule(1, 1, 1, 1)
    print(result)
    # One of the possible outputs: [[t1, m1, h1]]
    print(isBalancedSchedule(result, 1, 1, 1, 1))
    # Expected: true

def test3():
    print("===== Test 3 =====")
    result = Solution().buildBalancedSchedule(3, 1, 3, 2)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t2, m1, h2], [t3, m1, h3], [t2, m1, h1], [t3, m1, h2], [t1, m1, h3]]
    print(isBalancedSchedule(result, 3, 1, 3, 2))
    # Expected: true

def test4():
    print("===== Test 4 =====")
    result = Solution().buildBalancedSchedule(4, 3, 2, 2)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t1, m2, h2], [t2, m2, h1], [t2, m1, h2]]
    print(isBalancedSchedule(result, 4, 3, 2, 2))
    # Expected: true

def test5():
    print("===== Test 5 =====")
    result = Solution().buildBalancedSchedule(1, 3, 4, 1)
    print(result)
    # One of the possible outputs: [[t1, m1, h1], [t1, m2, h2], [t1, m3, h3], [t1, m1, h4]]
    print(isBalancedSchedule(result, 1, 3, 4, 1))
    # Expected: true

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()