# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")  

#Hands and deck
new_user_hand = []
dealer_hand = []
deck_of_cards = []

# initialize some useful global variables
in_play = False
outcome = " "
player_msg = "Hit or Stand ?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.user_hand = []

    def __str__(self):
        # return a string representation of a hand
        str = "Hand contains "
        for card in self.user_hand:
            str = str + card.suit + card.rank + " "
        return str

    def add_card(self, card):
        # add a card object to a hand
        self.user_hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        ace = 0
        for card in self.user_hand:
            value = value + VALUES[card.rank]
            if card.rank == "A":
                ace = 1
        if (value <= 11) and (ace == 1):
            value = value + 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        num = 0
        for card in self.user_hand:
            card.draw(canvas, [pos[0] + num * 90, pos[1]])
            num += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards_deck = []
        for i in SUITS:
            for j in RANKS:
                self.cards_deck.append(Card(i, j))
                

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards_deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards_deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        str = "Deck contains "
        for card in self.cards_deck:
            str = str + card.suit + card.rank + " "
        return str



#define event handlers for buttons
def deal():
    global outcome, in_play, new_user_hand, dealer_hand, deck_of_cards, player_msg, score
    if in_play:
        outcome = "Dealer Wins !."
        score -= 1
        in_play = False
    else:
        player_msg = "Hit or Stand ?"
        outcome = " "
        new_user_hand = Hand()
        dealer_hand = Hand()
        deck_of_cards = Deck()
        deck_of_cards.shuffle()
        new_user_hand.add_card(deck_of_cards.deal_card())
        new_user_hand.add_card(deck_of_cards.deal_card())
        dealer_hand.add_card(deck_of_cards.deal_card())
        dealer_hand.add_card(deck_of_cards.deal_card())
        in_play = True

def hit():
    global outcome, in_play, score, player_msg
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if in_play:
        value = new_user_hand.get_value() 
        if value < 21:
            new_user_hand.add_card(deck_of_cards.deal_card())
            value = new_user_hand.get_value()
            if value > 21:
                score = score - 1
                in_play = False
                outcome = "You Busted. Dealer wins !"
        elif value == 21:
            player_msg = "Already 21. Please Stand"
    
    
       
def stand():
    global outcome, in_play, score
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:	
        value1 = new_user_hand.get_value()
        if value1 <= 21:
            value2 = dealer_hand.get_value()
            while value2 < 17:
                dealer_hand.add_card(deck_of_cards.deal_card())
                value2 = dealer_hand.get_value()
            if value2 > 21:
                outcome = "Dealer Busted. You win !"
                score += 1
            else:
                if value1 > value2:
                    outcome = "You win !" 
                    score += 1
                else:
                    outcome = "Dealer Wins !"        
                    score -= 1
    in_play = False
    
def new_deal():
    global score, in_play
    in_play = False
    score = 0
    deal()
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [200, 75], 48, "Black")
    canvas.draw_text("Dealer", [50,175], 36, "Black")
    canvas.draw_text("Player", [50,375], 36, "Black")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [85.5, 248], CARD_BACK_SIZE)
        dealer_hand.user_hand[1].draw(canvas, [140, 198])
    else:
        dealer_hand.draw(canvas, [50, 200])
    new_user_hand.draw(canvas, [50, 400])
    canvas.draw_text("Score = " + str(score), [450, 50], 30, "Red")
    canvas.draw_text(outcome, [200, 175], 30, "Blue")
    if in_play:
        canvas.draw_text(player_msg, [200, 375], 30, "Red")
        


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("New Deal", new_deal, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
