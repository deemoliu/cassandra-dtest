from typing import List, Optional

"""
Design a fault-tolerant work queue whose tasks may be reserved for processing, completed, failed, retried, or moved to a dead-letter queue (DLQ).

Reserving a task temporarily assigns it for processing for a fixed lease duration. While the reservation is valid, the task is not available to be reserved again. If the task is not completed or explicitly failed before the lease expires, the reservation expires, and the task is retried or moved to the dead-letter queue according to its remaining attempts.

Every task begins in the ready state in the order given by taskIds. A completed or dead-lettered task never becomes ready again.

Implement the WorkQueue class:

WorkQueue(int[] taskIds, int leaseDuration, int maxAttempts) Initializes the queue.

taskIds contains the initial tasks in ready-queue order.
leaseDuration is the amount of logical time for which each successful reservation remains valid.
maxAttempts is the maximum number of times a task may be reserved, including its first reservation.
int[] reserve(int now) Reserves the task at the front of the ready queue for processing, where now is the current logical time. Return [taskId, reservationToken], or an empty array if no task is ready.

Each successful reservation receives a new positive reservationToken, beginning at 1 and increasing by 1 across the entire queue.
Reserving a task consumes one attempt.
The reservation expires at time now + leaseDuration and is valid only while the current logical time is strictly less than that expiration time.
boolean complete(int taskId, int reservationToken, int now) Marks a task as completed. Return true only if reservationToken identifies the task's current reservation and that reservation is still valid at time now. Otherwise, return false without changing the task.

boolean fail(int taskId, int reservationToken, int now) Explicitly fails the task's current reservation. Return true only if reservationToken identifies the task's current reservation and that reservation is still valid at time now.

If the task has attempts remaining, append it to the back of the ready queue.
Otherwise, move it to the dead-letter queue.
Return false without changing the task if the reservation is invalid, stale, or expired.
int[] getDeadLetterTaskIds(int now) Returns the dead-lettered task IDs in the order they entered the dead-letter queue, without removing them.

Before performing its own operation, every method that receives now must first process all reservations expiring at or before now. If multiple reservations expire, process them by increasing expiration time, breaking ties by increasing reservation token.

An expired reservation follows the same retry or dead-letter rule as an explicitly failed reservation. There is no background timeout worker, so expirations are processed only when one of these methods is called. Once a reservation expires, its token becomes stale and can no longer be used to complete or fail the task.

Input:
["WorkQueue", "reserve", "reserve", "complete", "reserve", "complete", "fail", "getDeadLetterTaskIds", "reserve"]
[[[10, 20], 3, 2], [0], [0], [20, 2, 1], [3], [10, 1, 3], [10, 3, 4], [4], [4]]

Output:
[null, [10, 1], [20, 2], true, [10, 3], false, true, [10], []]

Explanation:

WorkQueue queue = new WorkQueue(new int[]{10, 20}, 3, 2); // Initializes two ready tasks with a lease duration of 3 and at most 2 attempts.
queue.reserve(0); // Returns [10, 1]. Task 10 receives the first reservation.
queue.reserve(0); // Returns [20, 2]. Task 20 receives the second reservation.
queue.complete(20, 2, 1); // Returns true. Task 20 completes before its lease expires.
queue.reserve(3); // Returns [10, 3]. Task 10's first reservation expires at time 3, so it becomes ready for its second attempt.
queue.complete(10, 1, 3); // Returns false, because token 1 is stale.
queue.fail(10, 3, 4); // Returns true. This exhausts Task 10's attempts and moves it to the dead-letter queue.
queue.getDeadLetterTaskIds(4); // Returns [10].
queue.reserve(4); // Returns [], because no task is ready.

Hint
Begin by defining a precise state model for each task and tracking its reservation count against the maximum allowed attempts.
Use a min-heap sorted by expiration time to efficiently surface timed-out reservations as logical time progresses.
Process all pending expirations lazily at the start of each public method call to keep the ready queue and task states consistent.

Follow-up:
Extend the previous work queue so that tasks can depend on other tasks.

The dependency pairs are distinct, contain no self-dependencies, and form a directed acyclic graph (DAG). A task becomes ready only after all of its direct prerequisites have completed successfully. Until then, it remains blocked and cannot be reserved.

Implement the following changes to the WorkQueue class:

WorkQueue(int[] taskIds, int[][] dependencies, int leaseDuration, int maxAttempts) Initializes the queue with task dependencies.

Each dependencies[i] = [prerequisiteId, dependentId] means dependentId cannot become ready until prerequisiteId has completed successfully. Both task IDs appear in taskIds.
Tasks with no prerequisites begin ready in taskIds order. All other tasks begin blocked.
boolean complete(int taskId, int reservationToken, int now) Retains its behavior from the previous question. When a task completes successfully, it also satisfies that task as a prerequisite for its dependents.

A dependent becomes ready only when all of its direct prerequisites have completed successfully.
If one completion makes multiple tasks ready, append them to the ready queue in taskIds order.
The reserve, fail, and getDeadLetterTaskIds methods retain their behavior from the previous question, as do all lease, retry, reservation-token, timeout, and dead-letter rules.

A failed or expired reservation does not satisfy a dependency. If a prerequisite enters the dead-letter queue without completing successfully, any unfinished tasks that still depend on it remain blocked and receive no additional dead-letter action.
Input:
["WorkQueue", "reserve", "complete", "reserve", "reserve", "complete", "reserve", "complete", "reserve"]
[[[1, 2, 3, 4], [[1, 2], [1, 3], [2, 4], [3, 4]], 5, 2], [0], [1, 1, 1], [1], [1], [2, 2, 2], [2], [3, 3, 2], [2]]

Output:
[null, [1, 1], true, [2, 2], [3, 3], true, [], true, [4, 4]]

Explanation:

WorkQueue queue = new WorkQueue([1, 2, 3, 4], [[1,2],[1,3],[2,4],[3,4]], 5, 2); // Initializes Task 1 as ready. Tasks 2 and 3 depend on Task 1, and Task 4 depends on both Tasks 2 and 3.
queue.reserve(0); // Returns [1, 1].
queue.complete(1, 1, 1); // Returns true and makes Tasks 2 and 3 ready in taskIds order.
queue.reserve(1); // Returns [2, 2].
queue.reserve(1); // Returns [3, 3].
queue.complete(2, 2, 2); // Returns true, but Task 4 remains blocked because Task 3 is unfinished.
queue.reserve(2); // Returns [] because no task is ready.
queue.complete(3, 3, 2); // Returns true and releases Task 4.
queue.reserve(2); // Returns [4, 4].

Hint
Track how many unresolved prerequisites each task has left instead of re-evaluating the full list repeatedly.
Use a hash map to quickly identify which tasks are waiting on a just-completed prerequisite.
Maintain a separate index mapping each task ID to its original position to enforce deterministic ordering when unblocking.

"""
class WorkQueue:
    def __init__(self, taskIds: List[int], leaseDuration: int, maxAttempts: int):
        # TODO: Initialize WorkQueue

    def reserve(self, now: int) -> List[int]:
        # TODO: Implement reserve logic

    def complete(self, taskId: int, reservationToken: int, now: int) -> bool:
        # TODO: Implement complete logic

    def fail(self, taskId: int, reservationToken: int, now: int) -> bool:
        # TODO: Implement fail logic

    def getDeadLetterTaskIds(self, now: int) -> List[int]:
        # TODO: Implement getDeadLetterTaskIds logic