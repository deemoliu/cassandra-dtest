
"""
(This question is a variation of the LeetCode question 2408. Design SQL. If you haven't completed that question yet, it is recommended to solve it first.)

Design an in-memory SQL database system that supports creating tables, inserting data with dynamic type inference, and performing queries with filtering and sorting capabilities.

Implement the SQLManager class:

SQLManager() Initializes the empty database system.

void createTable(String tableName, List<String> columnNames) Creates a new table with the given tableName and a list of fixed columnNames.

The tableName is guaranteed to be unique.
Columns are initially untyped, but data inserted will be inferred as either integers or strings.
void insert(String tableName, List<String> values) Inserts a row into the specified table.

The row ID is auto-incremented starting from 0 for each table.
values corresponds to the column names defined during table creation (in the same order).
Your implementation must infer the data type. If a value represents a valid integer (e.g., "123"), it is treated as a number for comparison; otherwise, it is treated as a string.
List<Integer> select(String tableName, List<List<String>> conditions, List<String> orderBy) Selects rows from the table that satisfy all conditions (only consider "AND" logic) and returns their IDs in correct order.

conditions: A list of filters, where each filter is [<columnName>, <operator>, <value>].
Supported operators: "=" , ">" and "<" .
orderBy: A list of column names. Results should be sorted by these columns in ascending order.
If orderBy is empty, return rows in insertion order.
If two rows have the same value for the first order column, use the second, and so on.
Constraints:

1 ≤ columnNames.length ≤ 100
All queries are valid (referenced tables and columns always exist).
Example:

Input:
["SQLManager", "createTable", "insert", "insert", "insert", "insert", "select", "select", "select", "select"]

[[],
 ["users", ["name", "age"]],
 ["users", ["Alice", "30"]],
 ["users", ["Bob", "25"]],
 ["users", ["Charlie", "35"]],
 ["users", ["Mary", "25"]],
 ["users", [["age", ">", "28"]], []],
 ["users", [["age", ">", "25"], ["name", "<", "C"]], []],
 ["users", [["age", ">", "20"]], ["name"]],
 ["users", [["age", ">", "24"]], ["age", "name"]]]

Output:
[null, null, null, null, null, null, [0, 2], [0], [0, 1, 2, 3], [1, 3, 0, 2]]

Explanation:

SQLManager db = new SQLManager(); // Initializes the database.
db.createTable("users", ["name", "age"]); // Creates table "users".
db.insert("users", ["Alice", "30"]); // Inserts row with ID 0. "30" is treated as an integer.
db.insert("users", ["Bob", "25"]); // Inserts row with ID 1.
db.insert("users", ["Charlie", "35"]); // Inserts row with ID 2.
db.insert("users", ["Mary", "25"]); // Inserts row with ID 3.
db.select("users", [["age", ">", "28"]], []); // Returns [0, 2]. "Alice" (30) and "Charlie" (35) are > 28. "Bob" and "Mary" are not.
db.select("users", [["age", ">", "25"], ["name", "<", "C"]], []); // Returns [0]. Only "Alice" matches both.
db.select("users", [["age", ">", "20"]], ["name"]); // Returns [0, 1, 2, 3]. All match. Sorted by name: "Alice", "Bob", "Charlie", "Mary".
db.select("users", [["age", ">", "24"]], ["age", "name"]); // Returns [1, 3, 0, 2]. All match. Sorted by age first: "Bob" (25) and "Mary" (25) come before "Alice" (30) and "Charlie" (35). Tie-break for 25 uses name: "Bob" comes before "Mary".

Represent each table as a structured object that maps column names to their positional indices and maintains an ordered collection of inserted rows.

Before evaluating any condition or performing a sort, ensure both the stored cell value and the query parameter are explicitly converted to matching types to avoid lexicographical versus numerical com


"""

from typing import List, Optional

class SQLManager:
    def __init__(self, ):
        # TODO: Initialize SQLManager

    def createTable(self, tableName: str, columnNames: List[str]) -> None:
        # TODO: Implement createTable logic

    def insert(self, tableName: str, values: List[str]) -> None:
        # TODO: Implement insert logic

    def select(self, tableName: str, conditions: List[List[str]], orderBy: List[str]) -> List[int]:
        # TODO: Implement select logic
