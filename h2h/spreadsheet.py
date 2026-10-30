"""
(This question is a variation of the LeetCode question 3484. Design Spreadsheet. If you haven't completed that question yet, it is recommended to solve it first.)

Design a simplified spreadsheet that supports a grid of cells addressed like a standard spreadsheet: columns labeled A through Z and rows numbered 1 through 100. Each cell can hold a numeric value or a formula that references other cells.

Implement the Spreadsheet class:

Spreadsheet() Initializes the spreadsheet grid. All cells default to the value 0.0.

void setCell(String cell, String value) Stores a value in the cell identified by cell (e.g., "A1", "Z100").

value is either a non-negative numeric string (e.g., "1", "3.14") or a formula string beginning with "=".
A formula has the form =<term><op><term>, where each term is either a cell reference (e.g., A1) or a non-negative numeric literal, and <op> is one of '+', '-', '*', '/' (e.g., "=A1+5", "=A1-C3").
double getCell(String cell) Returns the current numeric value of cell as a double.

If cell has never been set, return 0.0.
If cell stores a numeric value, return that value.
If cell stores a formula, resolve all referenced cells at the time of this call.
Values computed during one getCell call do not persist to future calls, so any setCell updates in between are reflected correctly.
Constraints:

Column is a single uppercase letter 'A'-'Z'.
Row is an integer with 1 ≤ row ≤ 100.
Formulas contain exactly two terms and one operator ('+', '-', '*', '/'), with no whitespace.
Formulas do not contain parentheses or nested expressions.
Numeric strings and numeric literals are non-negative.
Division by zero will not occur.
It is guaranteed that the input contains no circular dependencies.
Example:

Input:
["Spreadsheet", "setCell", "setCell", "setCell", "setCell", "setCell", "getCell", "setCell", "getCell", "getCell"]
[[], ["B1", "3"], ["C1", "=B1+B1"], ["D1", "=C1+B1"], ["E1", "=C1*B1"], ["F1", "=D1+E1"], ["F1"], ["B1", "4"], ["F1"], ["C1"]]

Output:
[null, null, null, null, null, null, 27.0, null, 44.0, 8.0]

Explanation:

Spreadsheet sheet = new Spreadsheet();
sheet.setCell("B1", "3"); // B1 stores the literal value 3.
sheet.setCell("C1", "=B1+B1"); // C1 stores a formula depending on B1.
sheet.setCell("D1", "=C1+B1"); // D1 stores a formula depending on C1 and B1.
sheet.setCell("E1", "=C1*B1"); // E1 stores a formula depending on C1 and B1.
sheet.setCell("F1", "=D1+E1"); // F1 stores a formula depending on D1 and E1.
sheet.getCell("F1"); // Returns 27.0. C1 = 3 + 3 = 6, D1 = 6 + 3 = 9, E1 = 6 × 3 = 18, and F1 = 9 + 18 = 27. During this call, C1 is reachable through both D1 and E1, but it should be evaluated only once and reused.
sheet.setCell("B1", "4"); // B1 is overwritten with the literal value 4.
sheet.getCell("F1"); // Returns 44.0. The new call reflects the updated B1 value: C1 = 8, D1 = 12, E1 = 32, and F1 = 44.
sheet.getCell("C1"); // Returns 8.0.

Separate the raw storage of cell contents from the dynamic evaluation logic to keep the design clean and modular.
Use a depth-first search strategy to resolve cell references, and initialize a fresh memoization cache inside getCell to ensure calculations reflect the current state without leaking between calls.

Follow-up:
Continue with the optimized spreadsheet from the previous part. Now modify setCell to detect cycles before accepting a formula. The cell dependency graph must remain a DAG (Directed Acyclic Graph) at all times.

Update setCell as follows:

boolean setCell(String cell, String value) Stores value in the cell identified by cell (for example, "100" or "Z100"). When an update succeeds, any cells whose values depend on cell should reflect the updated value according to the spreadsheet's existing formula evaluation rules:
If value is a numeric string, the update succeeds and returns true.
If value is a formula, the update succeeds only if the resulting spreadsheet would not contain a circular dependency. If accepting the formula would create a cycle, reject the update, leave the spreadsheet and dependency graph unchanged, and return false.
All other behavior remains the same as in the previous part.

Constraints:

All constraints from the previous question still apply, except that callers may now submit formulas that would create cycles.
Example:

Input:
["Spreadsheet", "setCell", "setCell", "setCell", "getCell", "getCell"]
[[], ["A1", "1"], ["B1", "=A1+1"], ["A1", "=B1+1"], ["A1"], ["B1"]]

Output:
[null, true, true, false, 1.0, 2.0]

Explanation:

Spreadsheet sheet = new Spreadsheet();
sheet.setCell("A1", "1"); // Returns true.
sheet.setCell("B1", "=A1+1"); // Returns true. References A1. No path from A1 back to B1 exists, so no cycle. Formula is stored.
sheet.setCell("A1", "=B1+1"); // Returns false. References B1. Since B1 → A1 already exists, adding A1 → B1 would create the cycle A1 → B1 → A1. Update rejected.
sheet.getCell("A1"); // Returns 1.0. A1 still holds "1" (the rejected update left it unchanged).
sheet.getCell("B1"); // Returns 2.0. B1 = A1 + 1 = 1.0 + 1.0 = 2.0.

Before adding a new dependency edge, ask yourself what existing path between the referenced cell and the target cell would indicate a cycle.
Temporarily isolating the target cell from its previous outgoing edges during the check prevents outdated dependencies from causing false rejections.

"""

from typing import List, Optional

class Spreadsheet:
    def __init__(self, ):
        # TODO: Initialize Spreadsheet

    def setCell(self, cell: str, value: str) -> None:
        # TODO: Implement setCell logic

    def getCell(self, cell: str) -> float:
        # TODO: Implement getCell logic
