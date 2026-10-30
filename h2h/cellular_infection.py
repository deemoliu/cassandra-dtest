"""
(This question is a variation of the LeetCode question 994. Rotting Orange. If you haven't completed that question yet, it is recommended to solve it first.)

A research lab is monitoring the spread of a plant disease across a grid of plants. You are given an m x n grid where each plant is either healthy (0) or infected (1).

The disease spreads simultaneously across all plants each day. A healthy plant becomes infected if at least threshold of its 8 neighboring cells (including diagonals) are currently infected. Once a plant becomes infected, it remains infected forever.

Return the number of days until the epidemic stabilizes, meaning a full day passes with no new infections. If the grid is already stable, return 0.

Constraints:

1 ≤ grid.length ≤ 200
1 ≤ grid[i].length ≤ 200
grid is rectangular
1 ≤ threshold ≤ 8
Each cell is either 0 or 1
The answer fits in a 32-bit signed integer
Example 1:

Input:
grid = [[1,0,0],
        [0,0,0],
        [0,0,0]],
threshold = 1
Output: 2
Explanation: The inflection precoess are as follows:

On day 1, the three cells adjacent to the top-left corner become infected because each has at least one infected neighbor.
On day 2, the remaining five cells become infected.
After day 2, no further changes occur, so the epidemic stabilizes after 2 days.
Example 2:

Input: grid = [[1,0],[0,0]], threshold = 2
Output: 0
Explanation: No healthy cell has 2 or more infected neighbors, so no new infections occur.

Example 3:

Input: grid = [[1,1,0],[0,0,0],[0,0,0]], threshold = 2
Output: 3

Hint1: Maintain a separate counter for each healthy cell tracking its infected neighbors, and defer marking cells as infected until you have evaluated the entire grid for the current day.

Hint2: Initialize a queue with all starting infected cells and process it level-by-level, using the level boundaries to increment the day counter while applying the threshold rule uniformly.

Follow-up 1:
Now, immune plants are added to the grid. You are given an m x n grid where each plant can be healthy (0), infected (1), or immune (2).

The disease spreads simultaneously across all plants each day. A healthy plant becomes infected if at least threshold of its 8 neighboring cells (including diagonals) are currently infected. Immune plants cannot be infected and do not contribute to the infected-neighbor count. Once a healthy plant becomes infected, it stays infected forever.

Return the number of days until the epidemic ends, meaning a full day passes with no new infections among non-immune plants.

Constraints:

Each cell is 0, 1, or 2
Example 1:

Input:
grid = [[1,0,0],
        [0,2,0],
        [0,0,0]],
threshold = 1
Output: 3
Explanation: The center cell is immune and never changes.

On day 1, cells (0,1) and (1,0) become infected.
On day 2, cells (0,2), (1,2), and (2,0) become infected.
On day 3, cells (2,1) and (2,2) become infected.
After day 3, no healthy plant can be infected, so the epidemic ends after 3 days.
Example 2:

Input: grid = [[1,1],[2,0]], threshold = 2
Output: 1

Example 3:

Input: grid = [[1,2,0],[2,2,0],[0,0,0]], threshold = 2
Output: 0

Hint
To enforce simultaneous daily updates, avoid modifying the grid in-place during neighbor checks; instead, batch-process cells that reach the threshold after scanning the current day's infected set.
Maintain a parallel count matrix tracking how many currently infected neighbors each healthy cell has, and reset or update these counts carefully as the infection frontier expands.

Follow-up 2:
You are given a grid of plants where infection spreads to healthy plants based on infected neighbors and a threshold. Now, infected plants recover after a certain number of days.

Each infected plant remains contagious for exactly recoveryDays days starting from the day it becomes infected, then becomes immune and can never be infected again. Once a plant becomes immune, it is no longer contagious.

Return the number of days required for the system to become fully stable, meaning no plant will change state in the future (all infections have either spread completely or been blocked, and all infected plants have recovered).

 
Each plant can be infected at most once
Example 1:

Input:
grid = [[1,0,0],
        [0,0,0],
        [0,0,0]],
threshold = 1, recoveryDays = 2
Output: 4
Explanation: All plants become infected by day 2. A plant infected on day 0 becomes immune at the beginning of day 2. Plants infected on day 1 become immune at the beginning of day 3. Plants infected on day 2 become immune at the beginning of day 4. After day 4, no cell can change again, so the answer is 4.

Example 2:

Input: grid = [[1,0]], threshold = 1, recoveryDays = 1
Output: 2

Example 3:

Input: grid = [[1,2],[2,0]], threshold = 2, recoveryDays = 3
Output: 3

Hints
Store the exact day each cell gets infected so you can compute its expiration day on the fly without recalculating from scratch.
Use a day-indexed queue or hash map to batch-process recoveries before applying new infections, allowing you to skip idle days entirely.

Follow-up 3:
Using the same grid notation as before (0 = healthy, 1 = infected, 2 = immune), infected plants can now die instead of recovering.

When a healthy plant becomes infected, it may be marked as fatally infected. This depends on the number of infected plants among its 8 neighboring cells at the moment it becomes infected. If that number is at least deathThreshold, the newly infected plant is marked as fatally infected. Otherwise, it is treated as a normal infected plant.

A fatally infected plant behaves the same as any other infected plant while it remains infected. It can still spread the disease to healthy neighboring plants. However, when its infected period ends, it dies instead of becoming immune. A dead plant never changes state again and is no longer contagious.

For all plants that become infected on the same day, their fatal status is determined using the infected plants that already existed before that day's infections occur. Plants infected on the same day do not count as infected neighbors for each other.

Return an array [daysUntilEnd, finalDeadCount], where:

daysUntilEnd is the number of days until there are no infected plants left.
finalDeadCount is the total number of plants that died from the infection.
Constraints:

1 ≤ deathThreshold ≤ 8
Each cell is 0, 1, or 2
Example 1:

Input:
grid = [[1,0,0],
        [0,0,0],
        [0,0,0]],
threshold = 1, recoveryDays = 1, deathThreshold = 1
Output: [3, 8]
Explanation: The infection process is as follows:

Initially, only the top-left cell is infected. Since it has no infected neighbors when it first becomes infected, it is not marked as fatal.
On day 1, the original infected cell recovers and becomes immune. The three cells adjacent to the top-left corner become infected. Each of them has at least one infected neighbor in the previous day's state, so all three are marked as fatal.
On day 2, the three fatally infected cells from day 1 die. The remaining five healthy cells become infected. Each of them has at least one infected neighbor in the previous day's state, so all five are marked as fatal.
On day 3, the five fatally infected cells from day 2 die.
After day 3, there are no infected cells left, so the epidemic ends. The final dead count is 8, and only the original seed survives as immune.

Example 2:

Input: grid = [[1,0,0],[0,2,0],[0,0,0]], threshold = 1, recoveryDays = 2, deathThreshold = 8
Output: [5, 0]

Example 3:

Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], threshold = 1, recoveryDays = 3, deathThreshold = 3
Output: [6, 2]

Follow-up 4:
Using the same grid notation as before (0 = healthy, 1 = infected, 2 = immune), you may now create a one-time firebreak before the epidemic begins.

Before day 1 starts, you may choose one of the following options:

burn nothing,
burn exactly one full row,
or burn exactly one full column.
This burn decision is made only once, before any infection spreading happens. After the epidemic starts, no more rows or columns may be burned.

Every plant in the burned row or column is removed from the epidemic process. A burned plant can never become infected, is never contagious, and never changes state again. If a plant was already infected in the original grid but is burned, it no longer spreads the disease. Burned plants are not counted as deaths.

After this optional one-time burn, the epidemic follows the same rules as the previous problem. In particular, infection spread, recovery, immunity, and fatal infection are all handled exactly as before.

Your goal is to choose the best valid option, including the option to burn nothing, so that the final number of plants that die from infection is minimized. Return the minimum possible number of plants that die from infection.

Constraints:

Each cell is 0, 1, or 2
At most one row or one column may be burned
Burned plants are never infected, never contagious, and are never counted as deaths
Example 1:

Input:
grid = [[1,0,0],
        [0,0,0],
        [0,0,1]],
threshold = 1, recoveryDays = 1, deathThreshold = 1
Output: 4
Explanation: Burning the middle row is one optimal choice. The infection process after the burn is as follows:

Initially, the middle row is burned and removed from the epidemic process. The two infected seeds remain at the top-left and bottom-right corners.
On day 1, each seed recovers and becomes immune because recoveryDays = 1. The top-left seed infects the two healthy cells next to it in the top row, and the bottom-right seed infects the two healthy cells next to it in the bottom row. These four newly infected plants each have at least one infected neighbor at the moment of infection, so all four are marked as fatal.
On day 2, the four fatally infected plants die.
After day 2, there are no infected plants left, so the epidemic ends with 4 deaths. Since no single row or column can remove both original seeds, the minimum possible death count is 4.

Example 2:

Input: grid = [[1,0,0],[0,0,0],[0,0,0]], threshold = 1, recoveryDays = 1, deathThreshold = 1
Output: 0

Example 3:

Input: grid = [[1,1,0,0],[1,0,2,0],[0,2,0,1],[0,0,1,1]], threshold = 2, recoveryDays = 2, deathThreshold = 2
Output: 5

"""
from typing import List, Optional

class Solution:
    def daysToStabilize(self, grid: List[List[int]], threshold: int) -> int:
        # TODO: Implement daysToStabilize logic

    def daysToStabilizeWithImmunity(self, grid: List[List[int]], threshold: int) -> int:
        # TODO: Implement daysToStabilizeWithImmunity logic

    def daysToFullStabilityWithRecovery(self, grid: List[List[int]], threshold: int, recoveryDays: int) -> int:
        # TODO: Implement daysToFullStabilityWithRecovery logic

    def epidemicOutcomeWithDeaths(self, grid: List[List[int]], threshold: int, recoveryDays: int, deathThreshold: int) -> List[int]:
        # TODO: Implement epidemicOutcomeWithDeaths logic

    def minimumDeaths(self, grid: List[List[int]], threshold: int, recoveryDays: int, deathThreshold: int) -> int:
        # TODO: Implement minimumDeaths logic


