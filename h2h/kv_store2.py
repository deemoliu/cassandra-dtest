"""
Follow-up:
You are required to implement a persistent key-value store for string keys and values, with the added constraint that all stored data can be split and saved across multiple files, with each file being no larger than sizeLimit bytes.

When serializing the key-value store, if the binary data exceeds this size limit, it should be divided into multiple files or segments. During deserialization, the store must be able to correctly reconstruct its state by reading from all saved parts, ensuring that all key-value pairs are restored exactly as before.

You may modify the provided implementations of the saveBlob() and getBlob() methods in the InMemoryMedium class to support reading from and writing to multiple files as necessary.

/**
 * An in-memory implementation of the Medium interface.
 * Supports splitting data into multiple parts based on a size limit.
 */
class InMemoryMedium implements Medium {

    public InMemoryMedium(int sizeLimit){...}

    public void saveBlob(byte[] data) {...}

    public byte[] getBlob(){...}
}

Implement the KVStore class:

KVStore(Medium medium) Initializes a new, empty key-value store using the provided storage medium. The store only interacts with data via this medium.

void put(String key, String value) Stores the specified value associated with the given key. If the key already exists, its value is updated.

String get(String key) Returns the value associated with key. If the key is not present, it returns the empty string "".

void shutdown() Serializes the current store into a custom binary format and writes it to the associated medium, splitting the data into multiple parts of at most sizeLimit bytes each as needed. After shutdown, the instance becomes closed, any subsequent get or put must fail and throw an error.

void restore() Requests the complete logical byte stream from the medium by concatenating all saved parts in the correct order. And restores the in-memory store from this data, fully overwriting its contents.

Constraints:

All keys and values are ASCII strings.
Each file or persisted part must have size ≤ sizeLimit bytes.
1 ≤ number of keys ≤ 10⁴.
Total size of all persisted keys, values, and headers ≤ 10⁶ bytes.
Methods are called in a valid order.
Example:

Input:
["InMemoryMedium", "KVStore", "put", "put", "put", "put", "put", "get", "get", "get", "shutdown", "KVStore", "get", "put", "restore", "get", "get", "get", "get"]

[[64], [], ["user1", "Alice_Johnson_from_New_York"], ["user2", "Bob_Smith_from_Los_Angeles"], ["user3", "Charlie_Brown_from_Chicago"], ["user4", "Diana_Prince_from_San_Francisco"], ["user5", "Eve_Williams_from_Seattle"], ["user1"], ["user3"], ["user_nonexistent"], [], [], ["user1"], ["temp_key", "temp_value"], [], ["user1"], ["user2"], ["user5"], ["temp_key"]]

Output:
[null, null, null, null, null, null, "Alice_Johnson_from_New_York", "Charlie_Brown_from_Chicago", "", null, null, "", null, null, "Alice_Johnson_from_New_York", "Bob_Smith_from_Los_Angeles", "Eve_Williams_from_Seattle", ""]

Explanation:

Medium medium = new InMemoryMedium(64); Initialize medium with 64 bytes file size limit.
KVStore store1 = new KVStore(medium);
store1.put("user1", "Alice_Johnson_from_New_York"); // This entry is around 40 btyes after serizilation.
store1.put("user2", "Bob_Smith_from_Los_Angeles"); // Around 39 btyes.
store1.put("user3", "Charlie_Brown_from_Chicago"); // Around 38 btyes.
store1.put("user4", "Diana_Prince_from_San_Francisco"); // Around 42 bytes.
store1.put("user5", "Eve_Williams_from_Seattle"); // Around 38 btyes.
store1.get("user1"); // Returns "Alice_Johnson_from_New_York".
store1.get("user3"); // Returns "Charlie_Brown_from_Chicago".
store1.get("user_nonexistent"); // Returns "".
store1.shutdown(); // Serializes the data and distributes it across multiple files (approximately 197 bytes in total), requiring 3 or 4 files for storage.
KVStore store2 = new KVStore(medium); // New store using same medium.
store2.get("user1"); // Returns "" (not restored yet).
store2.put("temp_key", "temp_value"); // Adds "temp_key" temporarily.
store2.restore(); // Loads and restores all entries from all persisted parts.
store2.get("user1"); // Returns "Alice_Johnson_from_New_York".
store2.get("user2"); // Returns "Bob_Smith_from_Los_Angeles".
store2.get("user5"); // Returns "Eve_Williams_from_Seattle".
store2.get("temp_key"); // Returns "".

Start by implementing the core get and put logic using a standard hash map, completely ignoring the storage medium.
Decouple the problem by first serializing the entire map into one contiguous byte array, then iterating over that array to slice it into size-limited segments.
Track whether the store has been shut down with a boolean flag, and throw an immediate exception for any operation invoked after shutdown.

"""
import io
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# The Medium interface allows persisting and retrieving raw binary data.
class Medium(ABC):
    @abstractmethod
    def saveBlob(self, data: bytes) -> None:
        pass

    @abstractmethod
    def getBlob(self) -> Optional[bytes]:
        pass

# An in-memory implementation of the Medium interface for testing purposes.
# Supports splitting data into multiple parts based on a size limit.
class InMemoryMedium(Medium):
    def __init__(self, sizeLimit: int):
        self.sizeLimit = sizeLimit
        self.parts: List[bytes] = []

    def saveBlob(self, data: bytes) -> None:
        # TODO: Implement saveBlob logic.
        pass

    def getBlob(self) -> Optional[bytes]:
        # TODO: Implement getBlob logic.
        pass

class KVStore:
    def __init__(self, medium: Medium):
        # TODO: Implement __init__ logic.
        pass

    def put(self, key: str, value: str) -> None:
        # TODO: Implement put logic.
        pass

    def get(self, key: str) -> str:
        # TODO: Implement get logic.
        pass

    def shutdown(self) -> None:
        # TODO: Implement shutdown logic.
        pass

    def restore(self) -> None:
        # TODO: Implement restore logic.
        pass

    @staticmethod
    def main(args: List[str]) -> None:
        KVStore.test1()
        KVStore.test2()

    @staticmethod
    def test1() -> None:
        print("===== Test 1 =====")

        medium = InMemoryMedium(64)
        store1 = KVStore(medium)
        store1.put("user1", "Alice_Johnson_from_New_York")
        store1.put("user2", "Bob_Smith_from_Los_Angeles")
        store1.put("user3", "Charlie_Brown_from_Chicago")
        store1.put("user4", "Diana_Prince_from_San_Francisco")
        store1.put("user5", "Eve_Williams_from_Seattle")
        print(store1.get("user1"))  # Expected: "Alice_Johnson_from_New_York"
        print(store1.get("user3"))  # Expected: "Charlie_Brown_from_Chicago"
        print(store1.get("user_nonexistent"))  # Expected: ""
        store1.shutdown()

        store2 = KVStore(medium)
        print(store2.get("user1"))  # Expected: ""
        store2.put("temp_key", "temp_value")
        store2.restore()
        print(store2.get("user1"))  # Expected: "Alice_Johnson_from_New_York"
        print(store2.get("user2"))  # Expected: "Bob_Smith_from_Los_Angeles"
        print(store2.get("user5"))  # Expected: "Eve_Williams_from_Seattle"
        print(store2.get("temp_key"))  # Expected: ""

    @staticmethod
    def test2() -> None:
        print("\n===== Test 2 (Large Value) =====")

        medium = InMemoryMedium(32)
        store1 = KVStore(medium)

        # Create a large value that exceeds the size limit (500 characters)
        largeValue = []
        largeValue.append("ABCDEFGHIJ" * 50)
        largeData = "".join(largeValue)

        store1.put("large_key", largeData)
        store1.put("small_key", "small_value")
        print("Length: " + str(len(store1.get("large_key"))))  # Expected: 500
        print(store1.get("small_key"))  # Expected: "small_value"
        store1.shutdown()

        store2 = KVStore(medium)
        store2.restore()
        print("Length: " + str(len(store2.get("large_key"))))  # Expected: 500
        print(store2.get("small_key"))  # Expected: "small_value"
        store2.put("large_key", "updated_value")
        store2.put("new_key", "new_data")
        store2.shutdown()

        store3 = KVStore(medium)
        store3.restore()
        print(store3.get("large_key"))  # Expected: "updated_value"
        print(store3.get("new_key"))  # Expected: "new_data"

if __name__ == "__main__":
    KVStore.main([])
