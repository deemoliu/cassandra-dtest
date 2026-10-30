"""
Follow-up:
In this follow-up, you are again given a sorted ascending list of software versions in the format "MAJOR.MINOR.PATCH" (e.g., "103.3.2"), and you have access to a function isSupported() that tells you whether a version supports a specific feature or not.

Unlike the previous problem, where support was globally monotonic (once supported, always supported for all higher versions), here support is not globally monotonic across the entire list. Instead, the list exhibits a hierarchical monotonicity:

If a given "MAJOR" version group contains at least one version that supports the feature, then all subsequent "MAJOR" version groups (if any) will also eventually have at least one supporting version. However, support is not guaranteed for every individual version within those higher "MAJOR" groups, nor for all subsequent versions in general.

For example, if you discover that a 3.x.x version supports the feature, you can be certain that for every "MAJOR" version greater than 3 (if any), there will at some point be a version (such as 4.x.x, 5.x.x, etc., with potentially different MINOR or PATCH numbers) that also supports it.

The same hierarchical rule applies within "MINOR" groups of a given "MAJOR", and within "PATCH" groups of a given "MINOR".

Your task is to find the earliest version in the list that supports the feature, while minimizing the number of calls to isSupported API.

Implement the Solution class:

Solution(VersionChecker checker) Initializes your solution with the provided checker API.

String findEarliestSupported(List<String> versions) Returns the earliest version in versions that supports the feature, following the rules:

You must use the isSupported method from VersionChecker class to check each version.
It is guaranteed that at least one version in the list is supported.
Your implementation should minimize the number of calls to isSupported.
Constraints:

1 ≤ versions.length ≤ 
10
5
10 
5
 
Each version string is in the format "MAJOR.MINOR.PATCH".
0 ≤ "MAJOR", "MINOR", "PATCH" ≤ 
10
5
10 
5
 , and no part will have leading zeros.
The versions list is sorted in ascending order.
Example:
Input:
["Solution", "findEarliestSupported"]
["VersionChecker(["1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"])", ["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"]]

Output:
[null, "1.0.1"]

Explanation:

checker = new VersionChecker(["1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"]) // Creates a version checker that can determine whether a given version is supported, and the list of supported versions is unknown to you.
solution = new Solution(checker);
solution.findEarliestSupported(["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"]); // Returns "1.0.1", determined by making a series of isSupported calls.

Consider whether checking the final element of a subgroup is sufficient to determine if the answer lies within that group or an earlier/later one.
You can decompose the three-component version into three independent search dimensions, applying a narrowing strategy at each level.
Focus on establishing monotonicity at the group boundaries before recursively or iteratively drilling down into the next component level.
"""

from typing import List, Set

# External API that checks if a version supports a specific feature.
# You should NOT directly access the supported versions set.
class VersionChecker:
    def __init__(self, supportedVersions: Set[str]):
        self.supportedVersions = supportedVersions
        self.callCount = 0

    def isSupported(self, version: str) -> bool:
        self.callCount += 1
        return version in self.supportedVersions

    def getCallCount(self) -> int:
        return self.callCount

class Solution:
    def __init__(self, checker: VersionChecker):
        self.checker = checker

    def findEarliestSupported(self, versions: List[str]) -> str:
        # TODO: Implement findEarliestSupported logic.
        pass

def test1():
    print("===== Test 1 =====")
    supported = {"1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"}
    versions = ["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.1.0", "2.0.0"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 1.0.1
    print("Total calls: " + str(checker.getCallCount()))

def test2():
    print("\n===== Test 2 =====")
    supported = {"1.10.17", "1.10.18", "1.10.19", "1.11.1", "2.5.1"}
    versions = ["1.10.17", "1.10.18", "1.10.19", "1.11.0", "1.11.1", "2.0.0", "2.4.1",
                "2.4.2", "2.5.1"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 1.10.17
    print("Total calls: " + str(checker.getCallCount()))

def test3():
    print("\n===== Test 3 =====")
    supported = {"5.3.0", "5.3.5", "10.1.9", "15.7.8", "20.5.12"}
    versions = ["5.2.1", "5.2.3", "5.3.0", "5.3.5", "10.0.8", "10.1.2", "10.1.9",
                "15.7.3", "15.7.8", "20.5.12"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 5.3.0
    print("Total calls: " + str(checker.getCallCount()))

def test4():
    print("\n===== Test 4 =====")
    supported = {"7.2.0", "11.1.2", "11.3.1"}
    versions = ["3.1.5", "3.1.9", "3.2.0", "7.0.1", "7.0.3", "7.2.0", "11.0.0", "11.0.4",
                "11.1.0", "11.1.2", "11.3.1"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 7.2.0
    print("Total calls: " + str(checker.getCallCount()))

def test5():
    print("\n===== Test 5 =====")
    supported = {"30.1.5"}
    versions = ["10.0.0", "10.1.0", "20.0.0", "30.0.0", "30.1.0", "30.1.5"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 30.1.5
    print("Total calls: " + str(checker.getCallCount()))

def test6():
    print("\n===== Test 6 =====")
    supported = {"1.1.5", "1.1.6", "1.2.1", "2.0.0"}
    versions = ["1.0.0", "1.0.2", "1.1.0", "1.1.5", "1.1.6", "1.2.0", "1.2.1", "2.0.0"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 1.1.5
    print("Total calls: " + str(checker.getCallCount()))

def test7():
    print("\n===== Test 7 =====")
    supported = {"0.0.0", "0.0.1", "0.1.0", "1.0.0"}
    versions = ["0.0.0", "0.0.1", "0.1.0", "1.0.0"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 0.0.0
    print("Total calls: " + str(checker.getCallCount()))

def test8():
    print("\n===== Test 8 =====")
    supported = {"7.7.7"}
    versions = ["7.7.7"]
    
    checker = VersionChecker(supported)
    solution = Solution(checker)
    result = solution.findEarliestSupported(versions)
    print(result)  # Expected: 7.7.7
    print("Total calls: " + str(checker.getCallCount()))

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()