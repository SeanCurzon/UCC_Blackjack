import random
from card import Card


class Deck():
    """Creates a deck object"""
    def __init__(self):

        """'A','2','3','4','5','6','7','8','9','10','J','Q','K'"""
    
        self._deck = []
        self._faces = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
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
        return self._deck
	
	
    def shuffleDeck(self):
        """Shuffles the deck into a random order"""
        random.shuffle(self._deck)
            
    def __str__(self):
        return str(self._deck)
		
def main():

	deck = Deck()
	deck = deck.createDeck(1)
	deck = deck.shuffleDeck()
	return deck

if __name__ == "__main__":
	main()
