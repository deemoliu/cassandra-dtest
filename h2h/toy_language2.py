import re

"""
Follow-up:
You are working with the same Node and Function type system described previously, which includes primitive types, generics, and arbitrarily nested tuple types.

Your task is to implement a type inference utility:

Node inferReturnType(Function function, List<Node> params)
Given a function definition function and a list of concrete argument types params, this helper must:

Validate whether params align with the function's parameter types, allowing generics in the function signature to be mapped to concrete types.
If the match is successful, determine and return the concrete return type by substituting generics in the return type according to these mappings.
If there is any type mismatch, return null.
A valid match requires:

The number of arguments and parameters to be identical.
Generics in the function definition can appear in parameters or the return type, either directly or nested inside tuples.
Primitive type mismatches (such as "int" versus "char") are considered failures.
Each generic name must be consistently bound to a single concrete type throughout the entire matching process. Any scenario where the same generic would need to represent conflicting types (for example, both "int" and "char", or tuples with different structures) should result in a mismatch.
Tuple types are matched recursively: the tuple's structure, arity (the number of elements), and the types of each nested element (including deeply nested tuples) must all align exactly.
Your solution should infer and return the concrete return type for the given invocation if possible, or null if the arguments do not satisfy the rules above.

Constraints:

Both the function parameter list and the input params may contain arbitrarily nested tuples, but params are always concrete.
Each tuple contains at most 100 elements.
Primitive types are limited to "int", "char", "float". All other non-tuple type names must be valid generics of the form "T" followed by a digit.
Generics may be reused multiple times anywhere in the function definition, including nested tuples and the return type.
Example 1:

Input: Function: ["T1", "T2", "int", "T1"] -> ["T1", "T2"], params = ["int", "char", "int", "int"]
Output: A node stringified as "[int,char]"
Explanation: "T1" is bound to "int" (positions 1 and 4), "T2" is bound to "char". Substituting these bindings into the return type ["T1", "T2"] yields ["int", "char"].

Example 2:

Input: Function: ["int", "T1", ["T2", "int"]] -> "T1", params = ["int", ["int", "str"], ["float", "int"]]
Output: A node stringified as "[int,str]"

Example 3:

Input: Function: ["T1", "T2", "int", "T1"] -> ["T1", "T2"], params = ["int", "int", "int", "char"]
Output: null

Hint
Start by verifying argument count and top-level structural alignment before inspecting individual types.
Use a single hash map to track generic bindings as you traverse parameters and reject early if a generic resolves to conflicting types.
Implement a dedicated recursive comparator that updates the binding map on success, then reuse the same map to perform a second pass for substituting generics in the return type.

"""

class Node:
    def __init__(self, value_or_tuple):
        if isinstance(value_or_tuple, str):
            # for primitive or generic types
            self.value = value_or_tuple
            self.tuple = None
            self.isTuple = False
        else:
            # for tuple types
            self.value = None
            self.tuple = value_or_tuple
            self.isTuple = True

    def isTuple(self):
        return self.isTuple

    def getValue(self):
        return self.value

    def getTuple(self):
        return self.tuple

    def __str__(self):
        if not self.isTuple:
            return self.value
        else:
            sb = "["
            for i in range(len(self.tuple)):
                sb += str(self.tuple[i])
                if i < len(self.tuple) - 1:
                    sb += ","
            sb += "]"
            return sb

class Function:
    def __init__(self, params, returnType):
        self.params = params
        self.returnType = returnType

    def getParams(self):
        return self.params

    def getReturnType(self):
        return self.returnType

    def __str__(self):
        sb = "["
        for i in range(len(self.params)):
            sb += str(self.params[i])
            if i < len(self.params) - 1:
                sb += ","
        sb += "] -> "
        sb += str(self.returnType)
        return sb

class Solution:
    @staticmethod
    def inferReturnType(function, params):
        # TODO: Implement inferReturnType logic.

    @staticmethod
    def main():
        Solution.test1()
        Solution.test2()
        Solution.test3()
        Solution.test4()
        Solution.test5()
        Solution.test6()

    @staticmethod
    def test1():
        print("===== Test 1 =====")
        # Function: [T1, T2, int, T1] -> [T1, T2].
        # Params: [int, char, int, int]
        func = Function([Node("T1"), Node("T2"), Node("int"), Node("T1")],
                       Node([Node("T1"), Node("T2")]))
        params = [Node("int"), Node("char"), Node("int"), Node("int")]
        result = Solution.inferReturnType(func, params)
        print(result)  # Expected: "[int,char]"

    @staticmethod
    def test2():
        print("\n===== Test 2 =====")
        # Function: [int, T1, [T2, int]] -> T1.
        # Params: [int, [int, char], [float, int]]
        func = Function([Node("int"), Node("T1"),
                        Node([Node("T2"), Node("int")])], Node("T1"))
        params = [Node("int"), Node([Node("int"), Node("char")]),
                 Node([Node("float"), Node("int")])]

        result = Solution.inferReturnType(func, params)
        print(result)  # Expected: "[int,char]"

    @staticmethod
    def test3():
        print("\n===== Test 3 =====")
        # Function: [T1, T2, int, T1] -> [T1, T2].
        # Params: [int, int, int, char]
        func = Function([Node("T1"), Node("T2"), Node("int"), Node("T1")],
                       Node([Node("T1"), Node("T2")]))
        params = [Node("int"), Node("int"), Node("int"), Node("char")]
        result = Solution.inferReturnType(func, params)
        print(result)  # Expected: null

    @staticmethod
    def test4():
        print("\n===== Test 4 =====")
        # Function: [[T1, T2], [T2, T3], T3] -> [T1, [T2, T3]].
        # Params: [[int, char], [char, [float, int]], [float, int]]
        func = Function(
            [Node([Node("T1"), Node("T2")]),
             Node([Node("T2"), Node("T3")]), Node("T3")],
            Node([Node("T1"), Node([Node("T2"), Node("T3")])]))

        params = [Node([Node("int"), Node("char")]),
                 Node([Node("char"), Node([Node("float"), Node("int")])]),
                 Node([Node("float"), Node("int")])]

        result = Solution.inferReturnType(func, params)
        print(result)  # Expected: "[int,[char,[float,int]]]"

    @staticmethod
    def test5():
        print("\n===== Test 5 =====")
        # Function: [int, float] -> char.
        # Params: [int, char]
        func1 = Function([Node("int"), Node("float")], Node("char"))
        params1 = [Node("int"), Node("char")]
        result1 = Solution.inferReturnType(func1, params1)
        print(result1)  # Expected: null

    @staticmethod
    def test6():
        print("\n===== Test 6 =====")
        # Function: [int] -> int.
        # Params: []
        func2 = Function([Node("int")], Node("int"))
        params2 = []
        result2 = Solution.inferReturnType(func2, params2)
        print(result2)  # Expected: null
        print()

if __name__ == "__main__":
    Solution.main()