from typing import List, Optional

"""
Design a card game for two players. 
Deal one card at a time, 
alternating between Player 1 and Player 2, 
until each player has three cards. 
Record who receives each card, then report both hands and the result.

Each card has a rank and a suit. 
Ranks increase from "2" through "10", 
then "J", "Q", "K", and "A". 
A hand belongs to one of these categories, from strongest to weakest:

Three of a kind: All three cards have the same rank.
Pair: Exactly two cards have the same rank.
High card: All three cards have different ranks.
The stronger category wins. 
If both hands have the same category, 
compare three of a kind by the repeated rank, 
pairs by the pair rank and then the remaining card (the kicker), 
and high-card hands by their ranks from highest to lowest. 
The first unequal rank decides the winner.

Suits do not affect hand strength. 
If the hands have equal strength, the result is a draw.

Implement the CardGame class:

CardGame() creates a new game.
String dealCard(String card) gives card to the next player and returns the deal event. Player 1 receives the first card.
Each card consists of a rank from "2" through "10", "J", "Q", "K", or "A", followed by one suit letter: "C" for clubs, "D" for diamonds, "H" for hearts, or "S" for spades.
List<String> checkResult() returns both hands in deal order and the final result. Call it after all six cards have been dealt.
Use these exact strings in the method outputs:

Each dealCard call returns "Player 1 dealt <card>" or "Player 2 dealt <card>".
Each hand is "Player 1 hand: [<card>, <card>, <card>]" or "Player 2 hand: [<card>, <card>, <card>]".
The final entry is "Winner: Player 1", "Winner: Player 2", or "Draw".
Constraints:

Exactly six distinct cards are dealt in each game.
Example:

Input:
["CardGame", "dealCard", "dealCard", "dealCard", "dealCard", "dealCard", "dealCard", "checkResult"]
[[], ["8H"], ["8C"], ["8S"], ["8D"], ["KH"], ["QS"], []]

Output:
[null, "Player 1 dealt 8H", "Player 2 dealt 8C", "Player 1 dealt 8S", "Player 2 dealt 8D", "Player 1 dealt KH", "Player 2 dealt QS", ["Player 1 hand: [8H, 8S, KH]", "Player 2 hand: [8C, 8D, QS]", "Winner: Player 1"]]

Explanation:

CardGame game = new CardGame();
game.dealCard("8H"); // Returns "Player 1 dealt 8H".
game.dealCard("8C"); // Returns "Player 2 dealt 8C".
game.dealCard("8S"); // Returns "Player 1 dealt 8S".
game.dealCard("8D"); // Returns "Player 2 dealt 8D".
game.dealCard("KH"); // Returns "Player 1 dealt KH".
game.dealCard("QS"); // Returns "Player 2 dealt QS".
game.checkResult(); // Returns both hands and "Winner: Player 1". Both players have a pair of eights, and Player 1's king kicker outranks Player 2's queen kicker.

hint1
Extract and map card ranks to a consistent ordering system before storing them, ignoring suits entirely.
hint2
Count rank frequencies within each hand to quickly determine the category, then sort the relevant ranks to establish tie-breaking order.

Follow-up 1:
Extend the previous game with a flush: a three-card hand whose cards all have the same suit. The category order is now three of a kind > flush > pair > high card.

If both players have a flush, compare their ranks from highest to lowest. The first unequal rank decides the winner. All other rules from the previous question remain unchanged.

Example:

Input:
["CardGame", "dealCard", "dealCard", "dealCard", "dealCard", "dealCard", "dealCard", "checkResult"]
[[], ["2H"], ["9C"], ["6H"], ["9D"], ["JH"], ["AS"], []]

Output:
[null, "Player 1 dealt 2H", "Player 2 dealt 9C", "Player 1 dealt 6H", "Player 2 dealt 9D", "Player 1 dealt JH", "Player 2 dealt AS", ["Player 1 hand: [2H, 6H, JH]", "Player 2 hand: [9C, 9D, AS]", "Winner: Player 1"]]

Explanation:

CardGame game = new CardGame();
game.dealCard("2H"); // Returns "Player 1 dealt 2H".
game.dealCard("9C"); // Returns "Player 2 dealt 9C".
game.dealCard("6H"); // Returns "Player 1 dealt 6H".
game.dealCard("9D"); // Returns "Player 2 dealt 9D".
game.dealCard("JH"); // Returns "Player 1 dealt JH".
game.dealCard("AS"); // Returns "Player 2 dealt AS".
game.checkResult(); // Returns both hands and "Winner: Player 1". Player 1's three hearts form a flush, which outranks Player 2's pair of nines.

hints
Normalize card strings into comparable tuples of rank and suit early to avoid repeated parsing
Structure each hand into a standardized comparison tuple starting with its category rank, followed by sorted card ranks

Extend the previous game to allow each player to fold or continue after both players have received two cards. The fold decisions are provided as inputs. The game does not choose them from the cards.

Add the following method to CardGame:

void setFoldDecision(int playerId, boolean fold) records one decision for Player playerId, where playerId is 1 or 2.
If fold is true, the player folds; otherwise, the player continues.
This function will be called once per player after both players have received their first two cards (the fourth deal).
After both decisions are recorded:

If both fold, the game ends with no winner.
If exactly one folds, the other player wins. No third cards are dealt.
If both continue, deal one more card to each player in the original alternating order, then compare the completed hands using the previous question's rules. Equal-strength hands result in a draw.
Call checkResult() after both decisions and, if both players continue, after the sixth deal. It returns the decision events in call order, followed by both current hands and the result. Each deal event is returned by its dealCard call, as in the previous question. A game ending after a fold reports two cards in each hand.

Use these additional exact strings:

Decision events are "Player 1 folds", "Player 2 folds", "Player 1 continues", or "Player 2 continues".
If both players fold, the final entry is "No winner".
If both players continue and their completed hands have equal strength, the final entry remains "Draw".
Example:

Input:
["CardGame", "dealCard", "dealCard", "dealCard", "dealCard", "setFoldDecision", "setFoldDecision", "checkResult"]
[[], ["8H"], ["8C"], ["8S"], ["8D"], [1, false], [2, true], []]

Output:
[null, "Player 1 dealt 8H", "Player 2 dealt 8C", "Player 1 dealt 8S", "Player 2 dealt 8D", null, null, ["Player 1 continues", "Player 2 folds", "Player 1 hand: [8H, 8S]", "Player 2 hand: [8C, 8D]", "Winner: Player 1"]]

Explanation:

CardGame game = new CardGame();
game.dealCard("8H"); // Returns "Player 1 dealt 8H".
game.dealCard("8C"); // Returns "Player 2 dealt 8C".
game.dealCard("8S"); // Returns "Player 1 dealt 8S".
game.dealCard("8D"); // Returns "Player 2 dealt 8D".
game.setFoldDecision(1, false); // Player 1 continues.
game.setFoldDecision(2, true); // Player 2 folds.
game.checkResult(); // Returns the decision events, both two-card hands, and "Winner: Player 1". The game ends before any third cards are dealt.

Hint
Maintain explicit flags for card counts and fold status to prevent invalid state transitions during deal or check operations.
Store every interaction in a single ordered collection, ensuring decision events precede hand summaries and the final result only triggers when the game state is fully resolved.

"""

class Suit(Enum):
    CLUBS = "CLUBS"
    DIAMONDS = "DIAMONDS"
    HEARTS = "HEARTS" 
    SPADES = "SPADES"   

class Rank(Enum):
    CARDA = 1
    CARD2 = 2
    CARD3 = 3
    CARD4 = 4
    CARD5 = 5
    CARD6 = 6
    CARD7 = 7
    CARD8 = 8
    CARD9 = 9
    CARD10 = 10
    CARDJ = 11
    CARDQ = 12
    CARDK = 13

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank.value}{self.suit.value[0]}"

    def __repr__(self):
        return f"{self.rank.value} of {self.suit.value}"

class CardGame:
    def __init__(self, ):
        # TODO: Initialize CardGame

    def dealCard(self, card: str) -> str:
        # TODO: Implement dealCard logic

    def checkResult(self, ) -> List[str]:
        # TODO: Implement checkResult logic

    def setFoldDecision(self, playerId: int, fold: bool) -> None:
        # TODO: Implement setFoldDecision logic
