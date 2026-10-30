"""
Design a rectangular board with width columns and height rows. The board is initially empty. Coordinates are zero-indexed: in (x, y), x is the column and y is the row. Each rectangle is defined by its top-left corner (x1, y1) and bottom-right corner (x2, y2), including every cell on its boundaries.

Rectangles may overlap. At a cell covered by multiple active rectangles, the one added most recently appears on top. Each addition receives the next positive rectangle ID, starting at 1. An ID is never reused, even after its rectangle is removed.

Implement the RectangleBoard class:

RectangleBoard(int width, int height) initializes an empty board.
int addRectangle(int x1, int y1, int x2, int y2) adds the rectangle and returns its assigned ID.
boolean removeRectangle(int rectangleId) removes a rectangle by ID.
If the rectangle exists and is active, remove the entire rectangle and return true. This may reveal another rectangle beneath it.
If the ID does not exist or the rectangle is already removed, return false without changing the board.
int getAt(int x, int y) returns the ID of the topmost active rectangle covering (x, y), or -1 if that cell is empty.
Constraints:

1 ≤ width, height ≤ 50.
0 ≤ x1 ≤ x2 < width.
0 ≤ y1 ≤ y2 < height.
0 ≤ x < width and 0 ≤ y < height for every query.
At most 2,000 method calls are made on one board.
Example:

Input:
["RectangleBoard", "addRectangle", "addRectangle", "getAt", "removeRectangle", "getAt", "getAt", "removeRectangle"]
[[4, 3], [1, 0, 2, 1], [2, 1, 3, 2], [2, 1], [2], [2, 1], [3, 2], [2]]

Output:
[null, 1, 2, 2, true, 1, -1, false]

Explanation:

RectangleBoard board = new RectangleBoard(4, 3);
board.addRectangle(1, 0, 2, 1); // Returns 1.
board.addRectangle(2, 1, 3, 2); // Returns 2. Both rectangles cover (2, 1), with rectangle 2 on top.
board.getAt(2, 1); // Returns 2.
board.removeRectangle(2); // Returns true. Rectangle 1 becomes visible at (2, 1).
board.getAt(2, 1); // Returns 1.
board.getAt(3, 2); // Returns -1, because no active rectangle covers the cell.
board.removeRectangle(2); // Returns false, because rectangle 2 is no longer active.

Hints:
Consider using a hash map to store rectangle metadata for O(1) removal lookups instead of scanning a collection every time.
When querying a cell, iterating through your stored records in reverse insertion order naturally mimics a stack, allowing you to find the topmost layer quickly.

Follow-up 1:
Extend the previous board to support undoing changes. The board keeps a history of successful operations that modify its rectangles. Removing an active rectangle counts as a change even when another rectangle completely covers it. An unsuccessful removal and a getAt query do not enter the history.

Support the following function for RectangleBoard:

boolean undo() reverses the most recent recorded operation and returns true, or returns false if the history is empty.
Undoing an addition removes that rectangle.
Undoing a removal restores the rectangle with its original ID, covered cells, and overlap position.
A successful undo() consumes the history entry it reverses and does not create another entry. IDs assigned by later additions continue increasing even if an earlier addition has been undone.

All other functions, including addRectangle, removeRectangle, and getAt retain their behavior from the previous question.

Example:

Input:
["RectangleBoard", "addRectangle", "addRectangle", "removeRectangle", "undo", "getAt", "undo", "getAt", "undo", "undo"]
[[4, 3], [1, 0, 2, 1], [2, 1, 3, 2], [1], [], [2, 1], [], [2, 1], [], []]

Output:
[null, 1, 2, true, true, 2, true, 1, true, false]

Explanation:

RectangleBoard board = new RectangleBoard(4, 3);
board.addRectangle(1, 0, 2, 1); // Returns 1.
board.addRectangle(2, 1, 3, 2); // Returns 2. Rectangle 2 covers rectangle 1 at (2, 1).
board.removeRectangle(1); // Returns true, even though rectangle 2 remains visible at the shared cell.
board.undo(); // Returns true, restores rectangle 1 beneath rectangle 2.
board.getAt(2, 1); // Returns 2.
board.undo(); // Returns true and removes rectangle 2.
board.getAt(2, 1); // Returns 1.
board.undo(); // Returns true, removes rectangle 1.
board.undo(); // Returns false, because the history is empty.

hint: Consider using a simple boolean flag on each rectangle record to track its active state without modifying its original coordinate data.
Store operation metadata (rectangle ID and action type) in a dedicated stack so you can precisely restore or remove records upon calling undo.


Follow-up 2:
Extend the previous board so that a rectangle can be removed by selecting a cell. The selected cell identifies the topmost active rectangle covering it. Removing it deactivates the entire rectangle, not just its coverage at the selected cell.

Add the following method to RectangleBoard:

int removeAt(int x, int y) removes the selected rectangle and returns its ID. If no active rectangle covers (x, y), return -1 without changing the board or its undo history.
A successful removeAt call is one operation in the existing undo history. Undo restores the same rectangle to its original place in the overlap order.

Example:

Input:
["RectangleBoard", "addRectangle", "addRectangle", "removeAt", "getAt", "undo", "getAt", "removeAt"]
[[4, 3], [1, 0, 2, 1], [2, 1, 3, 2], [2, 1], [2, 1], [], [2, 1], [0, 2]]

Output:
[null, 1, 2, 2, 1, true, 2, -1]

Explanation:

RectangleBoard board = new RectangleBoard(4, 3);
board.addRectangle(1, 0, 2, 1); // Returns 1.
board.addRectangle(2, 1, 3, 2); // Returns 2. It appears above rectangle 1 at (2, 1).
board.removeAt(2, 1); // Returns 2, removes rectangle 2 from the board.
board.getAt(2, 1); // Returns 1.
board.undo(); // Returns true, restores rectangle 2 above rectangle 1.
board.getAt(2, 1); // Returns 2.
board.removeAt(0, 2); // Returns -1, because the cell is empty.

hints:
Consider how the chronological insertion order naturally acts as a visibility stack, where newer rectangles hide older ones.
Iterate through your stored rectangle records in reverse order to quickly locate the highest active cover, then delegate to your existing removal mechanism.

Follow-up 3:
Extend the previous board so that a single call can remove all active rectangles covering a given cell.

Add the following method to RectangleBoard:

int batchRemove(int x, int y) removes all active rectangles covering cell (x, y) and returns the number removed.
This includes rectangles hidden beneath the topmost one. Each selected rectangle is removed from the entire board, not just from that cell.
If at least one rectangle is removed, the entire call counts as one undoable operation. A single undo() restores all rectangles removed by that call, including their original IDs, covered cells, and overlap order.
If no active rectangles cover the cell, return 0 without adding a history entry.
Example:

Input:
["RectangleBoard", "addRectangle", "addRectangle", "batchRemove", "getAt", "batchRemove", "undo", "getAt", "getAt"]
[[4, 3], [1, 0, 2, 1], [2, 1, 3, 2], [2, 1], [2, 1], [2, 1], [], [2, 1], [1, 0]]

Output:
[null, 1, 2, 2, -1, 0, true, 2, 1]

Explanation:

RectangleBoard board = new RectangleBoard(4, 3);
board.addRectangle(1, 0, 2, 1); // Returns 1.
board.addRectangle(2, 1, 3, 2); // Returns 2.
board.batchRemove(2, 1); // Returns 2. Both rectangles cover this cell, although only rectangle 2 is visible.
board.getAt(2, 1); // Returns -1, because both overlapping rectangles are inactive.
board.batchRemove(2, 1); // Returns 0, and creates no history entry.
board.undo(); // Returns true, and restores rectangles 1 and 2 together.
board.getAt(2, 1); // Returns 2, because it was added later.
board.getAt(1, 0); // Returns 1.

Decouple rectangle metadata from its active/inactive state so you can quickly toggle visibility across the entire board without rebuilding coordinates.
Scan your storage list to collect IDs of active rectangles covering the target cell, mark them inactive, and push a single history record containing those IDs onto your stack only if the collection is

"""

from typing import List, Optional

class RectangleBoard:
    def __init__(self, width: int, height: int):
        # TODO: Initialize RectangleBoard

    def addRectangle(self, x1: int, y1: int, x2: int, y2: int) -> int:
        # TODO: Implement addRectangle logic

    def removeRectangle(self, rectangleId: int) -> bool:
        # TODO: Implement removeRectangle logic

    def getAt(self, x: int, y: int) -> int:
        # TODO: Implement getAt logic

    def undo(self, ) -> bool:
        # TODO: Implement undo logic

    def removeAt(self, x: int, y: int) -> int:
        # TODO: Implement removeAt logic

    def batchRemove(self, x: int, y: int) -> int:
        # TODO: Implement batchRemove logic