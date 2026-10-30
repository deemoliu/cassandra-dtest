"""
You are given an N x M integer grid board, where each cell contains a score. Rows and columns are zero-indexed. A player starts from the top-row cell (0, p) and must reach any cell in the bottom row.

From a cell (i, j), the player may move to any valid destination among:

(i + 1, j - 1) diagonally down-left.
(i + 1, j) straight down.
(i + 1, j + 1) diagonally down-right.
(i + 2, j) special straight down jump.
The move (i + 2, j) is a special jump and may be used at most K times. When a special jump is used, the skipped cell (i + 1, j) is not visited and does not contribute to the score.

The score of a path is the sum of the values of all visited cells, including the starting cell and the ending cell. Return the maximum score obtainable by any valid path from (0, p) to the bottom row.

Constraints:

1 ≤ N, M ≤ 200
board is rectangular, and every row has exactly M columns.
0 ≤ p < M
0 ≤ K ≤ N
-104 ≤ board[i][j] ≤ 104
Example 1:

Input: board = [[1, 2, 3, 4], [5, 6, 1, 2], [7, 8, 9, 1], [3, 2, 5, 6]], p = 1, K = 1
Output: 23
Explanation: One optimal path is (0, 1) -> (1, 1) -> (2, 2) -> (3, 3). The score is 2 + 6 + 9 + 6 = 23.

Example 2:

Input: board = [[1, 5, 1], [-100, -100, -100], [1, 50, 1], [1, 1, 200]], p = 1, K = 1
Output: 255

Example 3:

Input: board = [[2, 1, 3], [-5, 10, -1], [4, -2, 6]], p = 1, K = 0
Output: 17

Hint
Consider how the limited number of special jumps should influence your DP state definition beyond just row and column.
Since movement is strictly downward, processing the grid from the last row upward naturally builds solutions to overlapping subproblems.
Observe that transitions only reference immediate next rows, allowing you to collapse the 3D DP table into a constant number of rolling rows for O(MK) space.

Follow-up 1:
Building on the previous question, instead of returning only the maximum score, return one valid path that obtains the maximum possible score.

The returned path should be an array of coordinate pairs [row, col]. It must start with [0, p] and end at any cell in the bottom row.

The path must follow the same movement rules:

From (i, j), the player may move to (i + 1, j - 1), (i + 1, j), (i + 1, j + 1), or (i + 2, j).
The move (i + 2, j) is a special jump and may be used at most K times.
When a special jump is used, the skipped cell is not visited and should not appear in the returned path.
If multiple optimal paths exist, return any one of them.

Constraints:

Same as the previous question.
The returned path must follow the same movement and jump rules.
The returned path must achieve the maximum possible score.
Example 1:

Input: board = [[1, 2, 3, 4], [5, 6, 1, 2], [7, 8, 9, 1], [3, 2, 5, 6]], p = 1, K = 1
Output: [[0, 1], [1, 1], [2, 2], [3, 3]]
Explanation: Starting at (0, 1) with value 2, the path moves down to (1, 1) with value 6, then diagonally to (2, 2) with value 9, and finally to (3, 3) with value 6. The total score is 2 + 6 + 9 + 6 = 23, which is the maximum possible score.


Example 2:

Input: board = [[1, 5, 1], [-100, -100, -100], [1, 50, 1], [1, 1, 200]], p = 1, K = 1
Output: [[0, 1], [2, 1], [3, 2]]

Example 3:

Input: board = [[2, 1, 3], [-5, 10, -1], [4, -2, 6]], p = 1, K = 0
Output: [[0, 1], [1, 1], [2, 2]]

hints
Consider computing optimal scores backwards from the bottom row up to the start, which naturally handles the jump constraint without recursion overhead.
For each cell and remaining jump count, record which neighbor yields the highest cumulative score to enable deterministic backtracking later.
Since transitions only look ahead one or two rows, you can maintain just two rolling layers of DP states while storing move decisions separately for reconstruction.

Follow-up 2:
Building on the first question, return the number of distinct valid paths that obtain the maximum possible score.

Two paths are distinct if their sequences of visited coordinates differ.

Constraints:

Same as the first question.
Example 1:

Input: board = [[1, 2, 3, 4], [5, 6, 1, 2], [7, 8, 9, 1], [3, 2, 5, 6]], p = 1, K = 1
Output: 1
Explanation: The only maximum-score path is (0, 1) -> (1, 1) -> (2, 2) -> (3, 3).

Example 2:

Input: board = [[0], [0], [0]], p = 0, K = 1
Output: 2

Example 3:

Input: board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], p = 1, K = 0
Output: 7

Your DP state should capture enough information to resolve both the objective function and the counting requirement; consider storing a tuple of (best_score, path_count) at each cell.
When combining results from neighbor cells, strictly separate the logic for improving the score versus tying the current best score to ensure accurate path counting.
Notice that calculations for row `i` only rely on rows `i+1` and `i+2`; exploit this locality to reduce space usage by keeping only the necessary future rows in memory.

Follow-up 3:
Building on the previous questions, add bonus scoring rules to the path score.

The base score is still the sum of all visited cell values. In addition:

If two consecutive visited cells in the path have the same value, add X.
If three consecutive visited cells in the path are strictly increasing in value, add Y.
Consecutive cells are determined by path order, so a special jump still connects two consecutive visited cells. The skipped cell in a special jump is not visited and does not participate in bonus calculation.

Specifically, each qualifying adjacent pair contributes its own X bonus. Each qualifying length-3 consecutive window contributes its own Y bonus. Overlapping windows are counted separately.

Return the maximum adjusted score obtainable by any valid path from (0, p) to any cell in the bottom row.

Constraints:

Same as the first question.
0 ≤ X, Y ≤ 10000
Example 1:

Input: board = [[1, 2, 3], [2, 2, 4], [3, 5, 6]], p = 0, K = 0, X = 10, Y = 100
Output: 109
Explanation: One optimal path is (0, 0) -> (1, 1) -> (2, 2), with values 1, 2, 6. Its base score is 1 + 2 + 6 = 9. Since 1 < 2 < 6, the path receives the Y bonus, giving an adjusted score of 109.


Example 2:

Input: board = [[5, 1], [5, 1], [5, 1]], p = 0, K = 0, X = 10, Y = 100
Output: 35

Example 3:

Input: board = [[1, 5, 1], [-100, -100, -100], [1, 50, 1], [1, 1, 200]], p = 1, K = 1, X = 0, Y = 0
Output: 255

hint
Extend your DP state beyond just coordinates and remaining jumps to include information about the previously visited cell.
Since bonuses only depend on adjacent visited nodes, encoding the prior move's direction or coordinates is sufficient to evaluate them on-the-fly.
Process states row-by-row and reuse memory for upcoming layers, as each transition only looks ahead by one or two rows.

"""

from typing import List, Optional

class Solution:
    def maxScore(self, board: List[List[int]], p: int, K: int) -> int:
        # TODO: Implement maxScore logic

    def maxScorePath(self, board: List[List[int]], p: int, K: int) -> List[List[int]]:
        # TODO: Implement maxScorePath logic

    def countMaxScorePaths(self, board: List[List[int]], p: int, K: int) -> int:
        # TODO: Implement countMaxScorePaths logic    

    def maxScoreWithBonuses(self, board: List[List[int]], p: int, K: int, X: int, Y: int) -> int:
        # TODO: Implement maxScoreWithBonuses logic