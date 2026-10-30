"""
Every device on the public Internet is identified by an IPv4 address, written in dotted-decimal notation as "A.B.C.D", where A, B, C, and D are integers from 0 to 255. Conceptually, the four octets form a single 32-bit unsigned value.

You are asked to implement a simple, forward-only iterator that produces every address from a given starting point up to the absolute upper limit (255.255.255.255).

Implement the IPv4Iterator class:

IPv4Iterator(String startIp) Initializes the iterator with the startIp. The first address yielded by the iterator must be exactly startIp.

boolean hasNext() Returns true if there is at least one address left to be produced. Otherwise, returns false.

String next() Returns the current address as a string in dotted-decimal form, then advances the internal cursor to the next sequential address.

It is guaranteed that next() is called only when hasNext() returns true.
The iterator visits addresses in strict ascending order (e.g., after "x.y.z.255" comes "x.y.(z+1).0").
Constraints:

startIp is a valid IPv4 address string.
0 ≤ startIp ≤ 255.255.255.255.
The number of next() calls will not exceed the remaining addresses in the range.
Example

Input:
["IPv4Iterator", "next", "next", "next", "hasNext"]
[["255.255.255.253"], [], [], [], []]

Output:
[null, "255.255.255.253", "255.255.255.254", "255.255.255.255", false]

Explanation:

IPv4Iterator iterator = new IPv4Iterator("255.255.255.253");
iterator.next(); // Returns "255.255.255.253".
iterator.next(); // Returns "255.255.255.254".
iterator.next(); // Returns "255.255.255.255".
iterator.hasNext(); // Returns false.

hint1: Treat the IPv4 address as a single large integer where each octet represents a digit in base 256; incrementing this value naturally handles carry-over between octets.
hint2: When reconstructing the string, use bitwise shifts or repeated modulo/division by 256 to extract individual octets from the current numeric state.

Follow-up 1:
Networking tasks sometimes need to enumerate IPv4 addresses in reverse order, such as when reclaiming unused space or performing backward scans. In this follow-up question, you need to implement a backward-only iterator that starts at a given address and walks toward the absolute minimum (0.0.0.0).

Implement the ReverseIPv4Iterator class:

ReverseIPv4Iterator(String endIp, int step) Initializes the iterator with the endIp and a fixed step size. The first address yielded by the iterator must be exactly endIp.

boolean hasNext() Returns true if there is at least one address left to be produced. Otherwise, returns false.

String next() Returns the current address in dotted-decimal form, then moves the internal cursor backward by step addresses.

It is guaranteed that next() is called only when hasNext() returns true.
The iterator visits addresses in strict descending order (e.g., after "x.y.z.0" comes "x.y.(z-1).255" when step = 1).
Constraints:

endIp is a valid IPv4 address string.
0 ≤ endIp ≤ 255.255.255.255.
step ≥ 1.
The number of next() calls will not exceed the remaining addresses in the range.
Example

Input:
["ReverseIPv4Iterator", "next", "next", "next", "hasNext"]
[["10.0.0.5", 2], [], [], [], []]

Output:
[null, "10.0.0.5", "10.0.0.3", "10.0.0.1", true]

Explanation:

ReverseIPv4Iterator iterator = new ReverseIPv4Iterator("10.0.0.5", 2);
iterator.next(); // Returns "10.0.0.5".
iterator.next(); // Returns "10.0.0.3".
iterator.next(); // Returns "10.0.0.1".
iterator.hasNext(); // Returns true, since addresses below 10.0.0.1 still exist.


Consider how an IPv4 address can be mathematically collapsed into a single integer value within a fixed numerical range.
Maintain a single numeric cursor for iteration state and perform the string conversion only when next() is called to simplify boundary logic.

Follow-up 2:
CIDR (Classless Inter-Domain Routing) notation compresses a consecutive block of IPv4 addresses into one string in the format "<IP>/<prefix>" (e.g., "192.168.1.0/30"). The prefix is an integer n (0 - 32) where the left-most n bits are fixed, and the remaining 32 - n bits vary to form 
2
32
−
n
2 
32−n
  addresses.

This problem asks you to build an iterator that lists addresses in a given CIDR block at a fixed interval, starting from the network address and moving upward.

Implement the CIDRIterator class:

CIDRIterator(String cidr, int step) Initializes the iterator with the CIDR string and a fixed step size. It derives the first and last addresses and positions at the network address (all host bits zero).

boolean hasNext() Returns true if there is at least one address left to be produced. Otherwise, returns false.

String next() Returns the current address in dotted-decimal form, then advances the cursor forward by step addresses.

It is guaranteed that next() is called only when hasNext() returns true.
The iterator must always begin at the network address.
Constraints:

0 ≤ prefix ≤ 32
step ≥ 1
Example

Input:
["CIDRIterator", "next", "next", "next", "next", "next", "next", "hasNext"]
[["192.168.1.0/28", 3], [], [], [], [], [], [], []]

Output:
[null, "192.168.1.0", "192.168.1.3", "192.168.1.6", "192.168.1.9", "192.168.1.12", "192.168.1.15", false]

Explanation:

CIDRIterator iterator = new CIDRIterator("192.168.1.0/28", 3); // Initialize with CIDR "192.168.1.0/28" (16 addresses), step 3.
iterator.next(); // Returns "192.168.1.0".
iterator.next(); // Returns "192.168.1.3".
iterator.next(); // Returns "192.168.1.6".
iterator.next(); // Returns "192.168.1.9".
iterator.next(); // Returns "192.168.1.12".
iterator.next(); // Returns "192.168.1.15".
iterator.hasNext(); // Returns false. No address within the block remains at or after 192.168.1.18.

Convert the dotted-decimal IP address into a single 32-bit integer to simplify range math and stepping.
Use bitwise AND with a mask derived from the prefix length to zero out the host bits and find the true network start.

Follow-up 3:
A simplified IPv6-like address is formatted as eight dot-separated hexadecimal segments: "H1.H2.H3.H4.H5.H6.H7.H8"

Each segment 
H
i
H 
i
​
 is a 4-character lowercase hexadecimal string in the range "0000" to "ffff". The address is treated as one 128-bit number, where the right-most segment is the least significant segment.

For example:

"0000.0000.0000.0000.0000.0000.0000.0000" is the minimum address.
"ffff.ffff.ffff.ffff.ffff.ffff.ffff.ffff" is the maximum address.
Addresses increment sequentially. When a segment exceeds "ffff", it wraps to "0000" and carries into the segment on its left.

For example, the address after "0000.0000.0000.0000.0000.0000.0000.ffff" is "0000.0000.0000.0000.0000.0000.0001.0000".

This problem asks you to build an iterator that lists addresses starting from a given address and moving upward by a fixed interval.

Implement the IPv6Iterator class:

IPv6Iterator(String startIp, int step) Initializes the iterator with the starting hexadecimal IP address and a fixed step size.

boolean hasNext() Returns true if there is at least one address left to be produced. Otherwise, returns false.

String next() Returns the current address, then advances the cursor forward by step addresses.

It is guaranteed that next() is called only when hasNext() returns true.
The iterator stops after advancing past "ffff.ffff.ffff.ffff.ffff.ffff.ffff.ffff".
Constraints:

startIp is always a valid address in the described format.
Each address contains exactly 8 dot-separated hexadecimal segments.
Each segment contains exactly 4 lowercase hexadecimal characters.
step ≥ 1
Example

Input:
["IPv6Iterator", "next", "next", "next", "hasNext"]
[["ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffd", 1], [], [], [], []]

Output:
[null, "ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffd", "ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffe", "ffff.ffff.ffff.ffff.ffff.ffff.ffff.ffff", false]

Explanation:

IPv6Iterator iterator = new IPv6Iterator("ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffd", 1); // Initialize at the given address with step 1.
iterator.next(); // Returns "ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffd".
iterator.next(); // Returns "ffff.ffff.ffff.ffff.ffff.ffff.ffff.fffe".
iterator.next(); // Returns "ffff.ffff.ffff.ffff.ffff.ffff.ffff.ffff".
iterator.hasNext(); // Returns false. The iterator has advanced past the maximum address.

Instead of manipulating the address as a raw string, convert each segment into an integer to simplify mathematical operations.
When advancing by a step, simulate manual addition from right to left, carrying any overflow beyond 0xFFFF to the next segment on the left.

"""
from typing import List, Optional

class IPv4Iterator:
    def __init__(self, startIp: str):
        # TODO: Initialize IPv4Iterator

    # followup-1
    # def __init__(self, endIp: str, step: int):
    #     # TODO: Initialize ReverseIPv4Iterator

    def hasNext(self, ) -> bool:
        # TODO: Implement hasNext logic

    def next(self, ) -> str:
        # TODO: Implement next logic

class IPv6Iterator:
    def __init__(self, startIp: str, step: int):
        # TODO: Initialize IPv6Iterator

    def hasNext(self, ) -> bool:
        # TODO: Implement hasNext logic

    def next(self, ) -> str:
        # TODO: Implement next logic
