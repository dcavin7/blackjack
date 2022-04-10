# PYTHON TERMINAL BLACKJACK GAME
# Damian Cavin
# 09 April 2022

import random
import math

# THE DECK

# Credit to Global Tech Council for help with structure
# https://www.globaltechcouncil.org/python/how-to-make-a-deck-of-cards-with-python/

class Card:
    def __init__(self, val, suit):
        self.suit = suit
        self.val = val
    
    def __repr__(self):
        return "{v} of {s}".format(v = self.val, s = self.suit)

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def __repr__(self):
        return "A standard 52-card deck"

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]:
                self.cards.append(Card(v, s))

    def show(self): # for debugging
        for card in self.cards:
            print(card)

    def shuffle(self):
        # Fisher-Yates shuffle
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw_card(self):
        return self.cards.pop()

deck = Deck()

# PLAYERS

class Player:
    def __init__(self, name, funds = 1000):
        self.name = name
        self.hand = []
        self.funds = funds
        self.bet = 0
        self.score = 0
    
    def __repr__(self):
        return "{n}, player of Blackjack".format(n = self.name)

    def show_cards(self):
        for card in self.hand:
            print(card)

    # Actions

    def draw(self): # Initial draw
        self.hand = []
        self.hand.append(deck.draw_card())
        self.hand.append(deck.draw_card())

    def hit(self):
        self.hand.append(deck.draw_card())

    def stand(self):
        pass

    def double(self):
        self.bet = self.bet * 2
        self.hand.append(deck.draw_card())

def find_score(hand):
    score = 0
    for card in hand:
        if type(card.val) == int:
            score += card.val
        elif (card.val == "King") or (card.val == "Queen") or (card.val == "Jack"):
            score += 10
        elif card.val == "Ace":
            if score <= 10:
                score += 11
            else:
                score += 1
        else:
            print("This shouldn't happen. How did you get here?")
    return score

player = Player("Player")
dealer = Player("Dealer")

# GAMEPLAY FUNCTIONS

def new_game():
    player = Player("Player")
    dealer = Player("Dealer")
    print("\nWelcome to Blackjack!")

def round():
    print("\nYou have ${f} left.".format(f = player.funds))

    # Bet
    bet_complete = False
    while bet_complete == False:
        bet = input("How much would you like to bet? Please enter a whole number.\n")
        try:
            bet = int(bet)
            if (bet <= player.funds) & (bet > 0):
                print("Betting ${b}.".format(b = bet))
                player.bet = bet
                player.funds -= bet
                bet_complete = True
            elif bet > player.funds:
                print("Whoops, you only have ${f}. Betting the max amount.".format(f = player.funds))
                player.bet = player.funds
                player.funds = 0
                bet_complete = True
            elif bet <= 0:
                print("That's not how that works.")
            else:
                print("This shouldn't happen. Please let Damian know how you broke his game so he can fix it.")
        except:
            print("That's not a whole number. Try again.")

    # Deal
    ### Player
    player.draw()
    print("\nHere is your hand:")
    player.show_cards()

    player.score = find_score(player.hand)
    print("Your total is {s}.".format(s = player.score))

    ### Dealer
    dealer.draw()
    print("\nThe dealer's first card is the {c}.".format(c = dealer.hand[0]))

    dealer.score = find_score(dealer.hand)

    # Player Decision
    player_turn = True
    while player_turn == True:
        print("\nWhat would you like to do?")
        choice = input("Options: Hit, Stand, Double down\n").lower()
        if choice == "hit":
            player.hit()
            print("\nHere is your hand:")
            player.show_cards()
            player.score = find_score(player.hand)
            print("Your total is {s}.".format(s = player.score))
            if player.score > 21:
                print("You busted!\n")
                player_turn = False
        elif choice == "stand":
            print("You stand.\n")
            player_turn = False
        elif (choice == "double") or (choice == "double down"):
            print("You double down.")
            player.double()
            print("\nHere is your hand:")
            player.show_cards()
            player.score = find_score(player.hand)
            print("Your total is {s}.\n".format(s = player.score))
            if player.score > 21:
                print("You busted!\n")
            player_turn = False
        else:
            print("Whoops, I didn't quite catch that.\n")

    # Dealer Logic
    dealer_turn = True
    while dealer_turn == True:
        if dealer.score >= 17:
            dealer_turn = False
        else:
            dealer.hit()
            dealer.score = find_score(dealer.hand)

    print("Dealer's hand:")
    dealer.show_cards()
    print("Dealer's total is {s}.\n".format(s = dealer.score))

    # Outcome Logic
    if player.score > 21:
        print("You lose!")
    elif (player.score > dealer.score) or (dealer.score > 21):
        if (player.score == 21) & (len(player.hand) == 2):
            print("You got Blackjack! Payout is 3:2.\n")
            player.funds += (2.5 * player.bet)
            player.funds = int(math.floor(player.funds))
        else:
            print("You won!\n")
            player.funds += 2 * player.bet
    elif player.score < dealer.score:
        print("You lose!\n")
    elif player.score == dealer.score:
        print("It's a tie. Bet returned.\n")
        player.funds += player.bet
    else:
        print("How exactly did you end up here? This shouldn't happen.\n")

# GAMEPLAY
new_game()
playing = True
while playing == True:
    round()
    deciding = True
    while deciding == True:
        new_round = input("Would you like to play another round?\n").lower()
        if (new_round == "y") or (new_round == "yes") or (new_round == "yes.") or (new_round == "yes!"):
            deciding = False
        elif (new_round == "n") or (new_round == "no") or (new_round == "no.") or (new_round == "no!"):
            deciding = False
            playing = False
            print("\nOkay, bye!")
            print("You exit the table with ${f}.\n".format(f = player.funds))
        else:
            print("Sorry, I didn't quite catch that. Please answer yes or no.")
