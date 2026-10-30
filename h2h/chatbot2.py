"""
Follow-up:
Design a multi-channel chat system that supports both human users and automated bots.

The system must be extensible to allow adding new bot types without altering existing logic. It should handle multiple, independent channels, ensuring that each channel's state is completely isolated, such as a user's away status or taco count being tracked separately in each channel. All three bot types from the previous question should be supported.

Implement the ChatApp class to manage channels and handle message processing:

ChatApp() Initializes the chat system.
void createChannel(String channelName) Creates a new, isolated chat channel with the specified name. This channel is automatically configured with all supported bots.
void sendMessage(String channelName, String name, String text) A user specified by name sends a message with text content to the channelName. This action may trigger responses from one or more bots.
List<String> getMessages(String channelName) Returns a list of all messages for the specified channelName, in the exact order they were processed. This includes both user-sent messages and bot-generated responses.
Constraints:

Bot command messages (e.g., "/away", "/meet", "/givetaco") are guaranteed to be in a valid format if they match the command prefix.
The number of calls to createChannel will be between 1 and 1000.
The total number of calls to sendMessage will be between 0 and 1000.
Example:

Input:
["ChatApp", "createChannel", "createChannel", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "sendMessage", "getMessages", "getMessages"]

[[], ["general"], ["dev"], ["general", "Alice", "Hello"], ["general", "Bob", "Hi"], ["general", "Alice", "Nice job on your presentations"], ["general", "Cindy", "/givetaco @justin"], ["general", "Bob", "/givetaco @justin 2"], ["general", "Alice", "Bob let's meet"], ["general", "Bob", "/meet Alice"], ["general", "David", "/away out for lunch"], ["general", "Emily", "Anyone around?"], ["general", "Frank", "/meet David"], ["dev", "Alice", "/givetaco @justin 2"], ["general"], ["dev"]]

Output:
[null, null, null, null, null, null, null, null, null, null, null, null, null, null,
  ["Alice: Hello",
   "Bob: Hi",
   "Alice: Nice job on your presentations",
   "Cindy: /givetaco @justin",
   "TacoBot: @Cindy gave @justin 1 taco. @justin now has 1 taco.",
   "Bob: /givetaco @justin 2",
   "TacoBot: @Bob gave @justin 2 tacos. @justin now has 3 tacos.",
   "Alice: Bob let's meet",
   "Bob: /meet Alice",
   "MeetBot: Google Meet with @Bob, and Alice starting at /abc-def-123",
   "David: /away out for lunch",
   "AwayBot: David is away: out for lunch",
   "Emily: Anyone around?",
   "Frank: /meet David",
   "AwayBot: David is away: out for lunch",
   "MeetBot: Google Meet with @Frank, and David starting at /abc-def-123"],
  ["Alice: /givetaco @justin 2",
   "TacoBot: @Alice gave @justin 2 tacos. @justin now has 2 tacos."]]

Explanation:

ChatApp chatApp = new ChatApp();
chatApp.createChannel("general"); // Bots are now active in "general".
chatApp.createChannel("dev");
chatApp.sendMessage("general", "Alice", "Hello"); // Message added.
chatApp.sendMessage("general", "Bob", "Hi");
chatApp.sendMessage("general", "Alice", "Nice job on your presentations");
chatApp.sendMessage("general", "Cindy", "/givetaco @justin"); // Triggers TacoBot. @justin's "general" count is 1.
chatApp.sendMessage("general", "Bob", "/givetaco @justin 2"); // Triggers TacoBot. @justin's "general" count is 3.
chatApp.sendMessage("general", "Alice", "Bob let's meet");
chatApp.sendMessage("general", "Bob", "/meet Alice"); // Triggers MeetBot. Alice is not away.
chatApp.sendMessage("general", "David", "/away out for lunch"); // Triggers AwayBot. David is now away.
chatApp.sendMessage("general", "Emily", "Anyone around?");
chatApp.sendMessage("general", "Frank", "/meet David"); Triggers MeetBot. David is away, so AwayBot responds first, then MeetBot.
chatApp.sendMessage("dev", "Alice", "/givetaco @justin 2"); // Triggers TacoBot in "dev". @justin's "dev" count is 2 (isolated from "general").
chatApp.getMessages("general"); // Returns the 17 messages from the "general" channel as shown above.
chatApp.getMessages("dev"); // Returns the 2 messages from the "dev" channel as shown above.

Define a unified Bot interface that standardizes how bots receive messages and generate responses, keeping their internal states separate.
Use a Registry or Factory pattern to automatically instantiate and attach all supported bot types whenever a new channel is initialized.
Encapsulate channel-specific data like away statuses and taco counts directly within the Channel class to guarantee complete isolation from other channels.

"""

from typing import Dict, List, Callable, TypeVar, Type, Any
from collections import defaultdict

class ChatApp:
    def __init__(self):
        """TODO: Implement ChatApp.__init__ logic."""
        pass

    def createChannel(self, channelName: str):
        """TODO: Implement createChannel logic."""
        pass

    def sendMessage(self, channelName: str, name: str, text: str):
        """TODO: Implement sendMessage logic."""
        pass

    def getMessages(self, channelName: str) -> List[str]:
        """TODO: Implement getMessages logic."""
        pass

def test1():
    print("===== Test 1 =====")
    app = ChatApp()
    app.createChannel("general")
    app.createChannel("dev")

    app.sendMessage("general", "Alice", "Hello")
    app.sendMessage("general", "Bob", "Hi")
    app.sendMessage("general", "Alice", "Nice job on your presentations")
    app.sendMessage("general", "Cindy", "/givetaco @justin")
    app.sendMessage("general", "Bob", "/givetaco @justin 2")
    app.sendMessage("general", "Alice", "Bob let's meet")
    app.sendMessage("general", "Bob", "/meet Alice")
    app.sendMessage("general", "David", "/away out for lunch")
    app.sendMessage("general", "Emily", "Anyone around?")
    app.sendMessage("general", "Frank", "/meet David")
    app.sendMessage("dev", "Alice", "/givetaco @justin 2")

    print(app.getMessages("general"))
    # Expected: ["Alice: Hello",
    # "Bob: Hi",
    # "Alice: Nice job on your presentations",
    # "Cindy: /givetaco @justin",
    # "TacoBot: @Cindy gave @justin 1 taco. @justin now has 1 taco.",
    # "Bob: /givetaco @justin 2",
    # "TacoBot: @Bob gave @justin 2 tacos. @justin now has 3 tacos.",
    # "Alice: Bob let's meet",
    # "Bob: /meet Alice",
    # "MeetBot: Google Meet with @Bob, and Alice starting at /abc-def-123",
    # "David: /away out for lunch",
    # "AwayBot: David is away: out for lunch",
    # "Emily: Anyone around?",
    # "Frank: /meet David",
    # "AwayBot: David is away: out for lunch",
    # "MeetBot: Google Meet with @Frank, and David starting at /abc-def-123"]

    print(app.getMessages("dev"))
    # Expected: ["Alice: /givetaco @justin 2",
    # "TacoBot: @Alice gave @justin 2 tacos. @justin now has 2 tacos."]


def test2():
    print("\n===== Test 2 =====")
    app = ChatApp()
    app.createChannel("general")

    app.sendMessage("general", "Alice", "/away on vacation")
    app.sendMessage("general", "Bob", "/away sick today")
    app.sendMessage("general", "Charlie", "/meet Alice")
    app.sendMessage("general", "David", "Hello everyone")
    app.sendMessage("general", "Eve", "/meet Bob")

    print(app.getMessages("general"))
    # Expected: ["Alice: /away on vacation",
    # "AwayBot: Alice is away: on vacation",
    # "Bob: /away sick today",
    # "AwayBot: Bob is away: sick today",
    # "Charlie: /meet Alice",
    # "AwayBot: Alice is away: on vacation",
    # "MeetBot: Google Meet with @Charlie, and Alice starting at /abc-def-123",
    # "David: Hello everyone",
    # "Eve: /meet Bob",
    # "AwayBot: Bob is away: sick today",
    # "MeetBot: Google Meet with @Eve, and Bob starting at /abc-def-123"]


def test3():
    print("\n===== Test 3 =====")
    app = ChatApp()
    app.createChannel("channel1")
    app.createChannel("channel2")
    app.createChannel("channel3")

    app.sendMessage("channel1", "Alice", "/givetaco @Bob 3")
    app.sendMessage("channel1", "Charlie", "/away lunch break")
    app.sendMessage("channel2", "Alice", "/givetaco @Bob 5")
    app.sendMessage("channel3", "Dana", "/meet Alice")

    print(app.getMessages("channel1"))
    # Expected: ["Alice: /givetaco @Bob 3",
    # "TacoBot: @Alice gave @Bob 3 tacos. @Bob now has 3 tacos.",
    # "Charlie: /away lunch break",
    # "AwayBot: Charlie is away: lunch break"]

    print(app.getMessages("channel2"))
    # Expected: ["Alice: /givetaco @Bob 5",
    # "TacoBot: @Alice gave @Bob 5 tacos. @Bob now has 5 tacos."]

    print(app.getMessages("channel3"))
    # Expected: ["Dana: /meet Alice",
    # "MeetBot: Google Meet with @Dana, and Alice starting at /abc-def-123"]


if __name__ == "__main__":
    test1()
    test2()
    test3()