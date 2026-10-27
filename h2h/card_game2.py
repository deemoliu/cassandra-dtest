from typing import List, Optional
from enum import Enum
import random

"""
deal and sort
(1)How would you modify the sorting logic if the suit order needed to change dynamically based on game rules?
(2)Discuss the pros and cons of using library shuffle functions versus implementing the Fisher-Yates algorithm manually.
(3)How would you extend this design to support variable numbers of players or uneven card distributions?
play 
(4) How would you modify the rules to support a Trump suit mechanism?
(5) If players used optimal strategy to maximize their score, how would the card selection logic change?
(6) Analyze the time complexity of the simulation relative to the number of players and cards.
score
(7)How would you decouple the scoring rules from the game engine to allow easy configuration changes?
(8)What data structures would you choose if you needed to replay past tricks or implement an undo feature?
(9)How would you adapt this simulation to handle an arbitrary number of players or variable deck sizes?
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
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{" + f"{self.rank.value}:{self.suit.value}" + "}"

    def __repr__(self):
        return self.__str__()

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, playerCount):
        hands = [[] for _ in range(playerCount)]
        cardIndex = 0
        while cardIndex < len(self.cards):
            for i in range(playerCount):
                if cardIndex < len(self.cards):
                    hands[i].append(self.cards[cardIndex])
                    cardIndex += 1
        return hands

class Player:
    def __init__(self, id, hand=None):
        self.id = id
        self.hand = hand if hand is not None else []
    
    def __str__(self):
        return f"Player <{self.id}>"

    def sortCard(self):
        self.hand.sort(key=lambda card: (card.suit.value, card.rank.value))

    def playCard(self, starter, hasSuit):
        if not self.hand:
            return None
        
        if starter is None or hasSuit:
            return self.hand.pop(0)

        for i in range(len(self.hand)):
            if self.hand[i].suit == starter.suit:
                return self.hand.pop(i)
        
        # Can't follow suit, play a card
        return self.hand.pop(0)

    def hasSuit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False

class Game:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        self.playerScores = [0] * len(self.players)
    
    def dealAndSortHands(self):
        self.deck.shuffle()
        hands = self.deck.deal(len(self.players))
        for i in range(len(self.players)):
            self.players[i].hand = hands[i]
            print(str(self.players[i])+ ": " + str(len(self.players[i].hand)) + " cards\n")
            self.players[i].sortCard()

        for i in range(len(self.players)):  
            print(str(self.players[i])+ ": [" + ", ".join(str(card) for card in self.players[i].hand) + "]\n")
    
    def playTrickRounds(self):
        playerCount = len(self.players)

        for player in players:
            rounds = min(len(self.deck.cards), len(player.hand))
        
        starterIdx = 0
        for round in range(rounds):
            print("=== Round " + str(round + 1) + " ===")
            trick = []
            playerOrder = []
            for i in range(playerCount):
                playerOrder.append((starterIdx + i) % playerCount)
            starterCard = self.players[playerOrder[0]].playCard(None, False)
            print("Player " + str(self.players[playerOrder[0]].id) + " played " + str(starterCard))
            trick.append(starterCard)

            for i in range(1, playerCount):
                player = self.players[playerOrder[i]]
                hasSuit = player.hasSuit(starterCard.suit)
                played = player.playCard(starterCard, hasSuit)
                print("Player " + str(player.id) + " played " + str(played))
                trick.append(played)
            
            winner = self.getWinner(playerOrder, trick, starterCard)
            print(f"Player {str(self.players[winner].id)} wins the round")
            starterIdx = playerOrder.index(winner)
            points = self.calculateRoundPoints(trick)
            print(f"Round winner took {points} points")
            self.playerScores[self.players[winner].id -1] += points

    def getWinner(self, playerOrder, trick, starterCard):
        winnerIndex = 0

        suit = starterCard.suit
        for i in range(len(trick)):
            if trick[i].suit == suit and trick[i].rank.value > starterCard.rank.value:
                winnerIndex = i
        return playerOrder[winnerIndex]

    def calculateRoundPoints(self, trick):
        points = 0
        for card in trick:
            value = card.rank.value
            if value == 5:
                points += 5
            elif value == 10:
                points += 10
            elif value == 13:  # K
                points += 10
        return points

    def scoreAndPrintResults(self):
        for player in self.players:
            print(str(player) + ": " + str(self.playerScores[player.id -1]))
            

if __name__ == "__main__":
    player1 = Player(1)
    player2 = Player(2)
    player3 = Player(3)
    player4 = Player(4)

    players = [player1, player2, player3, player4]
    deck = Deck()
    game = Game(players, deck)

    game.dealAndSortHands()
    game.playTrickRounds()
    game.scoreAndPrintResults()