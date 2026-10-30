"""
Design a social network system that tracks follow relationships between users while maintaining the historical state through snapshots. The system should allow users to follow and unfollow each other over time, and provide the ability to query whether a specific follow relationship existed at any previous snapshot.

Implement the SocialNetwork class:

SocialNetwork() Initializes an empty social network.
void follow(int followerId, int followeeId) Records that user followerId begins following user followeeId in the current working state.
void unfollow(int followerId, int followeeId) Records that user followerId stops following user followeeId in the current working state.
int createSnapshot() Captures the current state of all follow relationships and returns a unique snapshot identifier. The first snapshot has ID 0, and subsequent snapshots increment by 1.

boolean isFollowing(int followerId, int followeeId, int snapId) Returns true if user followerId was following user followeeId at the time snapshot snapId was created; otherwise returns false.

Note: Your solution is expected to handle historical queries and data efficiently, even when thousands of snapshots have been created.

Constraints:

1 ≤ followerId, followeeId, userId ≤ 105
0 ≤ snapId < 105
At most 105 calls will be made in total to all operations.
Example

Input:
["SocialNetwork", "follow", "follow", "createSnapshot", "unfollow", "isFollowing", "isFollowing", "isFollowing"]
[[], [1, 2], [2, 1], [], [1, 2], [1, 2, 0], [2, 1, 0], [1, 2, 1]]

Output:
[null, null, null, 0, null, true, true, false]

Explanation:

SocialNetwork sn = new SocialNetwork();
sn.follow(1, 2); // User 1 follows User 2.
sn.follow(2, 1); // User 2 follows User 1.
sn.createSnapshot(); // Returns 0. This snapshot captures the mutual follow state.
sn.unfollow(1, 2); // User 1 unfollows User 2.
sn.isFollowing(1, 2, 0); // Returns true. Since the unfollow happened after snapshot 0, User 1 was still following User 2 at that time.
sn.isFollowing(2, 1, 0); // Returns true.
sn.isFollowing(1, 2, 1); // Returns false.

Instead of duplicating the entire social graph for every snapshot, focus on recording only the state changes for each individual follow relationship.
Maintain a separate chronological log for each unique follower-followee pair, storing pairs of (snapshotId, isActiveStatus) whenever the relationship changes.
To answer a historical query efficiently, apply binary search on the log's snapshot IDs to locate the latest update that occurred at or before the requested snapId.

Follow-up 1:
Now extend the SocialNetwork class to retrieve lists of a user's connections at any given historical snapshot.

Implement the following additional methods:

List<Integer> getFollowers(int userId, int snapId) Returns a list of user IDs who were following userId at the given snapshot. You may return the result in any order.

List<Integer> getFollowees(int userId, int snapId) Returns a list of user IDs whom userId was following at the given snapshot. You may return the result in any order.

Example

Input:
["SocialNetwork", "follow", "follow", "createSnapshot", "getFollowers", "getFollowees"]
[[], [1, 2], [3, 2], [], [2, 0], [1, 0]]

Output:
[null, null, null, 0, [1, 3], [2]]

Explanation:

SocialNetwork sn = new SocialNetwork();
sn.follow(1, 2); // User 1 follows User 2.
sn.follow(3, 2); // User 3 follows User 2.
sn.createSnapshot(); // Returns 0.
sn.getFollowers(2, 0); // Returns [1, 3]. Both User 1 and User 3 are following User 2 at snapshot 0.
sn.getFollowees(1, 0); // Returns [2]. User 1 is following User 2 at snapshot 0.

Maintain auxiliary sets for each user that track all users who have ever followed them or whom they have ever followed to limit the iteration scope.
Store the interaction history between any two users as a sorted list of snapshots where the relationship was active, enabling temporal verification.
Iterate only over the relevant candidate set and use binary search to determine if a specific relationship existed at the requested snapshot ID.


Follow-up 2:
Now extend the SocialNetwork class to recommend new users for a specific user to follow based on a "friends of friends" logic at a given snapshot.

Implement the following additional method:

List<Integer> recommendUsers(int userId, int snapId, int k) Recommends the top k users for userId to follow based on the state at snapId, following the rules below:
At snapshot snapId, recommendations are generated based on second-degree follow relationships. A user is considered a candidate if they are followed by at least one of userId's followees at snapshot snapId.

A user is considered invalid as a candidate if they are the original userId, or if they are already directly followed by userId at snapId.

Each valid candidate receives a score equal to the number of followees of userId who follow that candidate at the same snapshot. Candidates are then ordered in descending order of score. If multiple candidates share the same score, they are ordered by ascending user ID.

The result should contain at most the top k ranked candidates. If fewer than k valid candidates exist, return all available candidates.

Constraints:

1 ≤ k ≤ 100
Example

Input:
["SocialNetwork", "follow", "follow", "follow", "follow", "createSnapshot", "recommendUsers"]
[[], [1, 2], [1, 3], [2, 4], [3, 4], [], [1, 0, 1]]

Output:
[null, null, null, null, null, 0, [4]]

Explanation:

SocialNetwork sn = new SocialNetwork();
sn.follow(1, 2); // User 1 follows User 2.
sn.follow(1, 3); // User 1 follows User 3.
sn.follow(2, 4); // User 2 follows User 4.
sn.follow(3, 4); // User 3 follows User 4.
sn.createSnapshot(); // Returns 0.
sn.recommendUsers(1, 0, 1); // Returns [4]. User 1's followees at snapshot 0 are [2, 3]. Both User 2 and User 3 follow User 4, giving User 4 a count of 2. Since User 1 is not following User 4, it is the top recommendation.

Start by retrieving all direct followees for the target user at the given snapshot to establish your starting layer.
Use a hash map to tally how many of those followees point to each unconnected user.
Apply the custom comparator after filtering invalid candidates, then truncate the result to size k.
"""

from typing import List, Optional

class SocialNetwork:
    def __init__(self, ):
        # TODO: Initialize SocialNetwork

    def follow(self, followerId: int, followeeId: int) -> None:
        # TODO: Implement follow logic

    def unfollow(self, followerId: int, followeeId: int) -> None:
        # TODO: Implement unfollow logic

    def createSnapshot(self, ) -> int:
        # TODO: Implement createSnapshot logic

    def isFollowing(self, followerId: int, followeeId: int, snapId: int) -> bool:
        # TODO: Implement isFollowing logic

    def getFollowers(self, userId: int, snapId: int) -> List[int]:
        # TODO: Implement getFollowers logic

    def getFollowees(self, userId: int, snapId: int) -> List[int]:
        # TODO: Implement getFollowees logic

    def recommendUsers(self, userId: int, snapId: int, k: int) -> List[int]:
        # TODO: Implement recommendUsers logic
