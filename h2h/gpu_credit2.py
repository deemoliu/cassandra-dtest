"""
You are designing a system to manage GPU credits. Each credit grant has a unique ID and is valid during a specific time window. Credit grants may overlap in time.

Because of network delays, events such as adding or consuming credits may arrive and be processed out of order with respect to their timestamp. At any time, you may query the system for the total available credits at a particular timestamp or attempt to consume credits at a specified time.

Implement the CreditSystem class:

CreditSystem() Initializes the credit system.

void grantCredit(String id, int amount, int startTime, int expirationTime) Adds a new credit grant identified by id, with amount units. The grant is active during the interval [startTime, expirationTime), meaning it is valid at startTime and no longer valid at expirationTime. Credit grants may overlap.

void subtract(int amount, int timestamp) Records a credit usage event at timestamp. When replaying events in chronological order, this usage must be deducted from grants that are active at timestamp, starting from the grants that expire the soonest.

int getBalance(int timestamp) Returns the total available credits at timestamp after replaying all currently known grants and subtracting events in chronological order. If any subtract event at time t <= timestamp cannot be fully covered by the grants active at time t, return -1 instead.

Constraints:

No two operations (grantCredit or subtract) share the same timestamp.
All grants, usage events, and queries may arrive in any order.
The result of getBalance is based on all events known so far and may change after later calls.
All amount, startTime, and expirationTime are in the range [0, 1000].
Example:

Input:
["CreditSystem", "grantCredit", "getBalance", "grantCredit", "subtract", "subtract", "getBalance", "getBalance", "getBalance", "getBalance", "getBalance", "getBalance"]
[[], ["a", 3, 10, 60], [10], ["b", 2, 20, 40], [1, 30], [3, 50], [10], [20], [30], [35], [40], [50]]

Output:
[null, null, 3, null, null, null, 3, 5, 4, 4, 3, 0]

Explanation:

CreditSystem cs = new CreditSystem();
cs.grantCredit("a", 3, 10, 60); // Grants 3 credits for time [10, 59].
cs.getBalance(10); // Returns 3.
cs.grantCredit("b", 2, 20, 40); // Grants 2 credits for time [20, 39].
cs.subtract(1, 30); // Consumes 1 credit at t=30, deducted from the earliest-expiring grant ("b").
cs.subtract(3, 50); // Consumes 3 credits at t=50, only grant "a" is available.
cs.getBalance(10); // Returns 3. Only grant "a" active at t = 10.
cs.getBalance(20); // Returns 5. Both "a" and "b" are active at t = 20.
cs.getBalance(30); // Returns 4. Only 1 credit has been consumed at t = 30.
cs.getBalance(35); // Returns 4.
cs.getBalance(40); // Returns 3. Only "a" is active at t = 40.
cs.getBalance(50); // Returns 0. The remaining 3 credits are consumed.

Hint1
Since events arrive out of order, store them in separate collections and defer the actual calculation until a query arrives.
hint2:
When stepping through the timeline, you need a data structure that efficiently retrieves and removes grants based on their expiration times.
hint3:
During the simulation, always apply each subtraction to the active grant that expires earliest to ensure the most efficient credit usage.
"""
from typing import List, Optional

class CreditSystem:
    def __init__(self, ):
        # TODO: Initialize CreditSystem

    def grantCredit(self, id: str, amount: int, startTime: int, expirationTime: int) -> None:
        # TODO: Implement grantCredit logic

    def subtract(self, amount: int, timestamp: int) -> None:
        # TODO: Implement subtract logic

    def getBalance(self, timestamp: int) -> int:
        # TODO: Implement getBalance logic

