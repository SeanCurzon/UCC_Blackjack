from flask import Flask
from flask import render_template, Response, request, redirect, url_for
import hittest
import random
app = Flask(__name__)

class Card():
    """Creates card objects"""

    def __init__(self, name_of_card, face, suit):
        """initialises objects with a face name and a suit"""
        self._name = name_of_card
        self._face = face
        self._suit = suit
        #gives each card object a value according to there face
        if self._face == "A":
            self._cardValue = 11
        elif self._face == "J":
            self._cardValue = 10
        elif self._face == "Q":
            self._cardValue = 10
        elif self._face == "K":
            self._cardValue = 10
        elif self._face == "10":
            self._cardValue = 10
        else:
            self._cardValue = int(self._name[0])

    def __str__(self):
        return str(self._name)

class Deck():
    """Creates a deck object"""
    def __init__(self):

        """'A','2','3','4','5','6','7','8','9','10','J','Q','K'"""
    
        self._deck = []
        self._faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10','J','Q','K']
        self._suits = ['Diamonds','Clubs','Hearts','Spades']

    def createDeck(self, numDecks):
        """creates a deck with 52 * numDecks amount of card objects
           numDecks is used as more than 1 dck of cards can be used in a
           blackjack game (usually 4)"""
        i = 0
        while i < numDecks:
            i += 1
            for f in range(len(self._faces)):
                for s in range(len(self._suits)):
                    #append to the deck card objects
                    self._deck.append(Card(self._faces[f] + "of" + self._suits[s], self._faces[f],self._suits[s]))              
        random.shuffle(self._deck)
        return self._deck
    
    """
    def shuffleDeck(self):
        return random.shuffle(self._deck) """
            
    def __str__(self):
        return str(self._deck) 

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/hit/", methods=['GET', 'POST'])
def hit():
    hit_msg = hittest.hit()
    return render_template('index.html', message = hit_msg)

@app.route("/deck/", methods=['GET', 'POST'])
def deck():
    deck = Deck().createDeck(1)
    deck_msg = deck[0]
    return render_template('index.html',  message = deck_msg)
