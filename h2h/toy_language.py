"""
You are working with a toy language grammar that supports three kinds of types: primitives, generics, and tuples. This system is used for defining function types, including parameter and return types.

Primitive types: "int", "char", "float"
Generic types: Strings following the pattern "T" plus a digit, such as "T1", "T2". A generic can stand for any type, including a tuple.
Tuple types: Represented as a list of types, for example ["int", "T1", "char"]. Tuples may be nested, such as ["int", "char", ["int", "T1"]].
A Node represents either a primitive, a generic, or a tuple.

A Function is described by its parameter list, params, and its return type, returnType. Both parameters and return type are represented as Node objects.

Your task is to implement the string representation of these types, following the exact format below:

Node.toString() returns a string for the type:

For a primitive or generic, return its value directly, such as "int" or "T2".
For a tuple, return its children in square brackets, separated by commas, such as "[int,T1,char]". There should be no extra spaces between each child. Nested tuples must be handled recursively.
Function.toString() returns the function type as "[<param1>,<param2>,...] -> <returnType>", where parameters and return type are rendered using Node.toString().

Constraints:

All type names are valid.
The params list and tuple children may be empty.
Nesting is allowed to any depth within tuples.
Example 1:

Input: Node representing primitive type "int".
Output: "int"

Example 2:

Input: Node representing tuple ["int", "T1", "char"].
Output: "[int,T1,char]"

Example 3:

Input: Function with params ["int", "T1", ["int", "T2"]] and return type "T1"
Output: "[int,T1,[int,T2]] -> T1"

hint1: Consider how each node should independently know how to serialize itself, delegating work to its children when necessary.

hint2: For tuple nodes, gather the serialized strings of all children first, then join them with commas before wrapping in brackets.

hint3: Use a StringBuilder to efficiently build the output string during recursion, and verify that empty collections naturally produce '[]'.

"""

class Node:
    def __init__(self, value=None, tuple=None):
        if tuple is not None:
            self.tuple = tuple
            self.isTuple = True
        else:
            self.value = value  # for primitive or generic types
            self.isTuple = False

    def __str__(self):
        # TODO: Implement __str__ logic.


class Function:
    def __init__(self, params, returnType):
        self.params = params
        self.returnType = returnType

    def __str__(self):
        # TODO: Implement __str__ logic.


class Solution:
    @staticmethod
    def main():
        Solution.nodeTest()
        Solution.functionTest()

    @staticmethod
    def nodeTest():
        print("===== Node Test =====")

        node1 = Node("int")
        print(node1)  # Expected: "int"

        node2 = Node("char")
        print(node2)  # Expected: "char"

        node3 = Node("float")
        print(node3)  # Expected: "float"

        node4 = Node("T1")
        print(node4)  # Expected: "T1"

        node7 = Node(tuple=[Node("int"), Node("T1"), Node("char")])
        print(node7)  # Expected: "[int,T1,char]"

        node8 = Node(tuple=[Node("float"), Node("T3")])
        print(node8)  # Expected: "[float,T3]"

        node9 = Node(tuple=[Node("int"), Node("char"),
                           Node(tuple=[Node("int"), Node("T1")])])
        print(node9)  # Expected: "[int,char,[int,T1]]"

        node10 = Node(tuple=[Node("int"),
                            Node(tuple=[Node("char"), Node(tuple=[Node("float"), Node("T1")])])])
        print(node10)  # Expected: "[int,[char,[float,T1]]]"

        node11 = Node(tuple=[Node(tuple=[Node("int"), Node("char")]),
                            Node(tuple=[Node("T1"), Node("T2")]),
                            Node(tuple=[Node("float"), Node("T3")])])
        print(node11)  # Expected: "[[int,char],[T1,T2],[float,T3]]"

        node12 = Node(tuple=[Node("int")])
        print(node12)  # Expected: "[int]"

        node13 = Node(tuple=[])
        print(node13)  # Expected: "[]"

        node14 = Node(tuple=[Node(tuple=[Node("int")])])
        print(node14)  # Expected: "[[int]]"

    @staticmethod
    def functionTest():
        print("\n===== Function Test =====")

        func1 = Function([Node("int"), Node("T1"),
                         Node(tuple=[Node("int"), Node("T2")])], Node("T1"))
        print(func1)  # Expected: "[int,T1,[int,T2]] -> T1"

        func2 = Function([Node("char"), Node("float")], Node("int"))
        print(func2)  # Expected: "[char,float] -> int"

        func3 = Function(
            [Node(tuple=[Node("int"), Node("char")]), Node("T1"),
             Node(tuple=[Node("float"),
                        Node(tuple=[Node("T2"), Node("T3")])])],
            Node(tuple=[Node("int"), Node("T1")]))
        print(func3)  # Expected: "[[int,char],T1,[float,[T2,T3]]] -> [int,T1]"

        func4 = Function([Node("int")], Node("char"))
        print(func4)  # Expected: "[int] -> char"

        func5 = Function([], Node("int"))
        print(func5)  # Expected: "[] -> int"

        func6 = Function([Node("int"), Node(tuple=[])], Node("T1"))
        print(func6)  # Expected: "[int,[]] -> T1"

        func7 = Function([Node("int")], Node(tuple=[]))
        print(func7)  # Expected: "[int] -> []"


if __name__ == "__main__":
    Solution.main()