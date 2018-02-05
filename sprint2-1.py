import random

class Dealer:
    
    def __init__(self):
        deck = Deck()
        self._id = "dealer"
        self._deck = deck.createDeck(1)
        random.shuffle(self._deck)
        self._hand = Hand(self._id)
        self._handValue = self._hand._handValue
        self._handlst = []
        dealerHand1 = self.dealerHand()

    def dealerHand(self) :
        V = False
        while V != True :
            temp = self._deck[0]
            new_card = temp
            if len( self._hand) == 0 :
                print("Dealer 1st Card: %s \n" % (new_card))
            if new_card._name[0] == "A" :
                if self._handValue >= 11 :
                    new_card._cardValue = 1
            self._deck.remove(self._deck[0])
            self._deck.append(temp)
            self._hand.add(new_card)
            self._handlst += [new_card]
            self._handValue += new_card._cardValue
            if self._handValue > 21 :
                for item in self._handlst :
                    if item._name[0] == "A" :
                        self._handValue -= 10
            if self._handValue >= 17 and self._handValue <= 21:
                V = True
            elif self._handValue > 21:
                V = True
            else :
                temp = self._deck[0]
                new_card = temp
                self._deck.remove(self._deck[0])
                self._deck.append(temp)
                self._hand.add(new_card)
                self._handValue += new_card._cardValue
	
    def getNewCard(self):
        return self._deck[0]


class Card(Dealer):

    def __init__(self, name_of_card, face, suit):
        self._name = name_of_card
        self._face = face
        self._suit = suit
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

class Hand(Dealer):
    def __init__(self, playerId):
        self._ID = playerId
        self._hand = []
        self._handValue = 0

    def add(self, card):
        self._hand.append(card)

    def __len__(self):
        return len(self._hand)

    def __str__(self):

        s = ""
        for item in self._hand :
            s += str(item)
            s += ", "
        return s

class Deck(Dealer):
    def __init__(self):

        """'A','2','3','4','5','6','7','8','9','10','J','Q','K'"""

        self._deck = []
        self._faces = ['A', '5', 'J'] #['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self._suits = ['Diamonds','Clubs','Hearts','Spades']

    def createDeck(self, numDecks):
        i = 0
        while i < numDecks:
            i += 1
            for f in range(len(self._faces)):
                for s in range(len(self._suits)):
                    self._deck.append(Card(self._faces[f] + "of" + self._suits[s], self._faces[f],self._suits[s]))              
        return self._deck
	
	
    def shuffleDeck(self):
        random.shuffle(self._deck)
            
    def __str__(self):
        return str(self._deck)
        
class Player(Dealer):
    
    _id = 1
    playersList = []
    mainlst = {}
    
    def __init__(self, dealer):

        self._id = Player._id
        Player._id += 1
        (self._balance) = 1000
        self._hand = Hand(self._id)
        self._handValue = self._hand._handValue
        self._deck = dealer._deck
        self._playersList = Player.playersList
        self._playersList += [self._id]
        self._mainlst = Player.mainlst
        self._handlst = []
        

    def main_hit(self,dealer, player_id):
        # deal until hand has 2 cards
        if len(self._hand) < 2:
            self.hit()
            print ( "Total Hand Value: %i\n" % (self._handValue))
        else:
            # busts when total hand value is greater than 21
            if self._handValue > 21:
                print("BUST")
                self.bust(player_id)
            
            else:
                hitorstay = input("Do you want to Hit or Stay? Hit/Stay ")
                if hitorstay == "h":
                    self.hit()
                    if self._handValue > 21 :
                        for item in self._handlst :
                            if item._name[0] == "A" :
                                self._handValue -= 10
                    print ( "Total Hand Value: %i\n" % (self._handValue))
                    self.main_hit( dealer, player_id)
                elif hitorstay == "s":
                    self.stay(dealer, player_id, self._handValue)

    """
    def split( self, dealer, player_id ) :

        # fix split on ace
    
        count = 0
        while count < 2 :
            self._hand.add(self._handlst[0])
            self.main_hit(dealer, player_id)
            count += 1 """


    def startingHand(self, dealer):
        self.bet(self._id)
        i = 0
        while i < 2:
            i += 1
            Hand(self._id)
            self.main_hit(dealer, self._id)
        self.main_hit(dealer, self._id)  

    def bet(self, player_id):
        self._bet = int(input("How much would player %s like to bet? " %player_id))


    def hit(self):
        temp = self._deck[0]
        new_card = temp
        if new_card._name[0] == "A" :
            if self._handValue >= 11 :
                new_card._cardValue = 1
        self._deck.remove(self._deck[0])
        self._deck.append(temp)
        self._hand.add(new_card)
        self._handlst += [new_card]
        print(new_card)
        self._handValue += new_card._cardValue

    def bust(self, player_id):
        print("Player %s went bust \n" % (player_id))

    def stay(self, dealer, player_id, hand_value):
        self._mainlst[player_id] = [hand_value, self._bet, self._balance]
        print(self._mainlst)
        print("Player %s stayed on Value = %i \n" % (player_id, hand_value))

    def compareHandAgainstDealer(self, dealer, mainlst) :

        print ( "Dealer Hand: %s" % ( dealer._hand))
        print ( "Dealer Score: %i" % (dealer._handValue))

        for item in mainlst :
            if mainlst[item][0] > dealer._handValue :
                print ( "Player %i Score: %i" % (item,mainlst[item][0]))
                print ( "You win\n" )
                (mainlst[item][2]) += (mainlst[item][1])
                print("Balance: %i" % (mainlst[item][2]))
            elif dealer._handValue > 21 :
                print ("Dealer Bust \n")
                print ("You win \n")
                (mainlst[item][2]) += (mainlst[item][1])
                print("Balance: %i" % (mainlst[item][2]))
            elif mainlst[item][0] == dealer._handValue :
                print ( "Draw, your bet has been refunded\n")
                print("Balance: %i" % (mainlst[item][2]))
            else :
                print ( "Player %i Score: %i" % (item, mainlst[item][0]))
                print ("You Lose\n")
                (mainlst[item][2]) -= mainlst[item][1]
                print("Balance: %i" % (mainlst[item][2]))

def main():

    dealer = Dealer()
    player1 = Player(dealer)
    player2 = Player(dealer)
    player3 = Player(dealer)
    player4 = Player(dealer)

    playerlst = [player1,player2,player3,player4]

    for item in playerlst :
        item.startingHand(dealer)

    player4.compareHandAgainstDealer(dealer, player4._mainlst)
    
if __name__ == "__main__":
    main()
    
