"""
(This question is a variation of the LeetCode question 362. Design Hit Counter. If you haven't completed that question yet, it is recommended to solve it first.)

Design a message-event aggregator for a long-running system. Each event identifies a user and a chat and has a timestamp measured in whole seconds. For any user and query timestamp, report the number of recorded events in the trailing window of m seconds. The window is inclusive and equals [timestamp - m + 1, timestamp].

Events for the same user arrive in strictly increasing timestamp order. The system must remain memory-efficient over an indefinite runtime by discarding history that can no longer affect future queries.

Implement the ChatEventAggregator class:

ChatEventAggregator(int m) Initializes the aggregator with the positive window length m, measured in seconds.
void processEvent(String userId, String chatId, int timestamp) Records one event for userId in chatId at timestamp.

int getChatCount(String userId, int timestamp) Returns the number of the user's recorded events with timestamps in [timestamp - m + 1, timestamp]. Return 0 when the user has no events in that window.

Constraints:

userId and chatId are non-empty strings.
A getChatCount query is not earlier than that user's most recently processed event.
Example:

Input:
["ChatEventAggregator", "processEvent", "processEvent", "processEvent", "getChatCount", "getChatCount", "getChatCount", "processEvent", "getChatCount", "processEvent", "getChatCount"]

[[5], ["u-1", "c-101", 10], ["u-1", "c-102", 11], ["u-1", "c-101", 14], ["u-1", 14], ["u-1", 15], ["u-2", 15], ["u-1", "c-103", 16], ["u-1", 16], ["u-1", "c-104", 19], ["u-1", 19]]

Output:
[null, null, null, null, 3, 2, 0, null, 2, null, 2]

Explanation:

aggregator = new ChatEventAggregator(5); // Initializes a five-second window.
aggregator.processEvent("u-1", "c-101", 10);
aggregator.processEvent("u-1", "c-102", 11);
aggregator.processEvent("u-1", "c-101", 14);
aggregator.getChatCount("u-1", 14); // Returns 3, because timestamps 10, 11, and 14 are in [10, 14].
aggregator.getChatCount("u-1", 15); // Returns 2, because timestamps 11 and 14 are in [11, 15].
aggregator.getChatCount("u-2", 15); // Returns 0, because that user has no recorded events.
aggregator.processEvent("u-1", "c-103", 16);
aggregator.getChatCount("u-1", 16); // Returns 2, because timestamps 14 and 16 are in [12, 16].
aggregator.processEvent("u-1", "c-104", 19);
aggregator.getChatCount("u-1", 19); // Returns 2 because timestamps 16 and 19 are in [15, 19].

Since timestamps for each user arrive in strictly increasing order, a double-ended queue naturally maintains chronological order and allows O(1) removal from the front.
You do not need to wait for a query to free memory; use the monotonic property to prune expired timestamps exactly when new events are recorded.
For queries, leverage the sorted nature of your storage to quickly identify the window boundary instead of rescanning the entire history.

Follow-up 1:
Extend the previous aggregator so that every event has an EventType: "INTERACT" or "END_CHAT". A user's chat is active when its most recent relevant event is "INTERACT" and an "END_CHAT" event makes that chat inactive. Report the number of distinct active chats for a user in the trailing window.

Implement the ChatEventAggregator class:

ChatEventAggregator(int m) Initializes the aggregator with the positive window length m, measured in seconds.

void processEvent(String userId, String chatId, int timestamp, String eventType) Records an "INTERACT" or "END_CHAT" event for one user-chat pair at timestamp.

int getActiveChatCount(String userId, int timestamp) Returns the number of distinct chats that satisfy the active-chat rule at timestamp. Return 0 when no chat is active.

The system must be memory-efficient and cannot retain expired chats or historical events that can no longer affect future queries. All definitions, ordering requirements, and identifier and timestamp constraints from the previous question still apply.

Example:

Input:
["ChatEventAggregator", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount", "getActiveChatCount"]

[[5], ["u-1", "c-101", 10, "INTERACT"], ["u-1", 10], ["u-1", "c-102", 11, "INTERACT"], ["u-1", 11], ["u-1", "c-101", 12, "END_CHAT"], ["u-1", 12], ["u-1", "c-103", 14, "INTERACT"], ["u-1", 14], ["u-1", 15]]

Output:
[null, null, 1, null, 2, null, 1, null, 2, 2]

Explanation:

aggregator = new ChatEventAggregator(5); // Initializes a five-second window.
aggregator.processEvent("u-1", "c-101", 10, INTERACT);
aggregator.getActiveChatCount("u-1", 10); // Returns 1, because "c-101" is "INTERACT" in [6, 10].
aggregator.processEvent("u-1", "c-102", 11, INTERACT);
aggregator.getActiveChatCount("u-1", 11); // Returns 2, because "c-101" and "c-102" are "INTERACT" in [7, 11].
aggregator.processEvent("u-1", "c-101", 12, END_CHAT);
aggregator.getActiveChatCount("u-1", 12); // Returns 1, because "c-101" is "END_CHAT" and only "c-102" remains "INTERACT" in [8, 12].
aggregator.processEvent("u-1", "c-103", 14, INTERACT);
aggregator.getActiveChatCount("u-1", 14); // Returns 2, because "c-102" and "c-103" are "INTERACT" in [10, 14].
aggregator.getActiveChatCount("u-1", 15); // Returns 2, because "c-102" and "c-103" remain active in [11, 15].

Maintain a direct lookup from each (userId, chatId) pair to its latest event type and timestamp to instantly determine if a chat is active.
Use a per-user collection of timestamps to quickly identify and discard any events falling outside the [timestamp - m + 1, timestamp] boundary.
Avoid recalculating the active count from scratch on every query by incrementally updating a counter as events enter or leave the valid window.

Follow-up 2:
Extend the active-chat aggregator to support events that may arrive out of timestamp order. Each user's event timestamps remain unique, and an event is accepted only when it falls within a bounded lateness window of m seconds.

For a user, let maxSeen be the greatest event timestamp processed so far, or 0 before any event. An event with a timestamp earlier than maxSeen - m + 1 is too late and must be ignored. Accepted events are applied in event-time order when determining each chat's active state. All other active-chat behavior and memory-efficiency requirements remain unchanged from the previous question.

Implement the ChatEventAggregator class:

ChatEventAggregator(int m) Initializes the aggregator with the positive window length and lateness bound m, measured in seconds.

void processEvent(String userId, String chatId, int timestamp, String eventType) Accepts an "INTERACT" or "END_CHAT" event unless it is too late under the user's current maxSeen boundary.

int getActiveChatCount(String userId, int timestamp) Returns the number of distinct chats whose latest accepted event in the trailing window is "INTERACT".

Constraints:

Calls to processEvent may arrive out of timestamp order.
Event timestamps are unique for each user.
Events earlier than maxSeen - m + 1 are ignored.
Example:

Input:
["ChatEventAggregator", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount", "processEvent", "getActiveChatCount"]

[[5], ["u-1", "c-101", 12, "END_CHAT"], ["u-1", 12], ["u-1", "c-101", 10, "INTERACT"], ["u-1", 12], ["u-1", "c-102", 11, "INTERACT"], ["u-1", 12], ["u-1", "c-103", 14, "INTERACT"], ["u-1", 14]]

Output:
[null, null, 0, null, 0, null, 1, null, 2]

Explanation:

aggregator = new ChatEventAggregator(5); // Initializes a five-second window and lateness bound.
aggregator.processEvent("u-1", "c-101", 12, "END_CHAT");
aggregator.getActiveChatCount("u-1", 12); // Returns 0, because "c-101"'s only event is "END_CHAT".
aggregator.processEvent("u-1", "c-101", 10, "INTERACT");
aggregator.getActiveChatCount("u-1", 12); // Returns 0, because the later event at 12 still leaves "c-101" inactive.
aggregator.processEvent("u-1", "c-102", 11, "INTERACT");
aggregator.getActiveChatCount("u-1", 12); // Returns 1, because "c-102" is "INTERACT" in event-time order while "c-101" ends with "END_CHAT".
aggregator.processEvent("u-1", "c-103", 14, "INTERACT");
aggregator.getActiveChatCount("u-1", 14); // Returns 2, because "c-102" and "c-103" are both "INTERACT".

Consider using a data structure that automatically maintains chronological order as new events arrive.
The acceptance boundary shifts dynamically based on the largest timestamp processed for each user, not the current query time.
Pair timestamp-based ordering with periodic cleanup to ensure both correctness and memory efficiency.

"""

from typing import List, Optional

class ChatEventAggregator:
    def __init__(self, m: int):
        # TODO: Initialize ChatEventAggregator

    def processEvent(self, userId: str, chatId: str, timestamp: int) -> None:
        # TODO: Implement processEvent logic

    def getChatCount(self, userId: str, timestamp: int) -> int:
        # TODO: Implement getChatCount logic

    def getActiveChatCount(self, userId: str, timestamp: int) -> int:
        # TODO: Implement getActiveChatCount logic
