import random
from hand import Hand


class Player():
    """Creates a Player object initialized with the following attributes"""
    
    _id = 1
    playersList = []
    mainlst = {}
    
    def __init__(self, dealer):
        """Initializes the object with the below attributes"""

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
        """Deals the current player 2 cards and then waits for the players response
            to hit or stay
            if the first 2 cards have the same value the function split is called."""

        main_boolean = True
        # deal until hand has 2 cards
        if len(self._hand) < 2:
            self.hit()
            print ( "Total Hand Value: %i\n" % (self._handValue))
        #when theres 2 cards dealt check if the values are equal
        elif len(self._hand) == 2:
            if self._handlst[0]._cardValue == self._handlst[1]._cardValue:
                spl = input("Do you want to split? y/n: ")
                #if player chooses to split call the split function
                if spl == 'y':
                    # checks if balance is sufficient enough for split.
                    if (self._bet * 2) > self._balance:
                        print("Split unavailable, insufficient funds!")
                        self.check_hand(dealer, player_id, main_boolean)
                    else:
                        self.split(dealer, self._id)
                    #else continue as usual
                elif spl == 'n':
                    self.check_hand(dealer, player_id, main_boolean)
            #checks if first two cards dealt are both Aces
            elif self._handlst[0]._name and self._handlst[1]._name[0] == "A":
                spl = input("Do you want to split? y/n: ")
                #if player chooses to split call the split function
                if spl == 'y':
                    # checks if balance is sufficient enough for split.
                    if (self._bet * 2) > self._balance:
                        print("Split unavailable, insufficient funds!")
                        self.check_hand(dealer, player_id, main_boolean)
                    else:
                        self._hand._hand[0]._cardValue = 11
                        self._hand._hand[1]._cardValue = 11
                        self._handValue = 22
                        self.split(dealer, self._id)
                    #else continue as usual
                elif spl == 'n':
                    self.check_hand(dealer, player_id, main_boolean)
            else:
                self.check_hand(dealer, player_id, main_boolean)
        else:
            self.check_hand(dealer, player_id, main_boolean)
            

    def split_hit(self,dealer, player_id):
        """Deals the current player 2 cards to each hand
           after the original hand has been split and then waits for the players
           response to hit or stay"""
        
        main_boolean = False
        # deal until hand has 2 cards
        if len(self._hand) < 2:
            self.hit()
            print ( "Total Hand Value: %i\n" % (self._handValue))
        else:
            # busts when total hand value is greater than 21
            self.check_hand(dealer, player_id, main_boolean)

    def check_hand(self, dealer, player_id, main_boolean):
        """Checks if the hand value is greater than 21
           If not askes player do they want to hit or stay"""
        
        #if the player busts call the bust function
        if self._handValue > 21:
            print("BUST")
            self.bust(player_id, self._handValue)
        else:
            hitorstay = input("Do you want to Hit or Stay? Hit/Stay ")
            #if the player  hits call the hit function
            if hitorstay == "h":
                self.hit()
                if self._handValue > 21 :
                        for item in self._handlst :
                            if item._name[0] == "A" :
                                item._cardValue = 1
                                self.countPlayerHand()
                print ( "Total Hand Value: %i\n" % (self._handValue))
                #checks if the check_hand function was called from split_hit or main_hit
                #if called from main_hit call main_hit
                if main_boolean == True:
                    self.main_hit( dealer, player_id)
                #else call split_hit
                else:
                    self.split_hit( dealer, player_id)
            #else call stay
            elif hitorstay == "s":
                    self.stay(dealer, player_id, self._handValue)

    def split( self, dealer, player_id ) :
        """Splits the users hand into 2 hands
           plays both hands out"""
        
        #store the second card in temp for use in the second hand to be made later
        temp = self._hand._hand[1]
        self._hand.remove(temp)
        self._handlst.remove(temp)
        print(self._handlst)
        self._handValue -= temp._cardValue
        
        #Playing out the first hand
        print("Hand 1: ", self._hand)
        print("Hand 1 value: ", self._handValue)
        i = 0
        while i < 2:
            i += 1
            self.split_hit(dealer, player_id)
        #self.main_hit(dealer, player_id)
        score = self._handValue
        print("Score: ", score)
        if score > 21:
            self._balance -= self._bet
        elif dealer._handValue > 21:
            self._balacne += self._bet
        elif score < dealer._handValue:
            self._balance -= self._bet
        elif score > dealer._handValue:
            self._balance += self._bet
        #clear the hand,handlst,set hand value to 0
        self._handlst = []
        self._hand.empty()
        self._handValue = 0
        #add the stored second card into the hand and handlst and set the value to the
        #cards value
        self._hand.add(temp)
        self._handlst += [temp]
        self._handValue += temp._cardValue
        
        #Playing out the second hand
        print("Hand 2: ", self._hand)
        print("Hand 2 value: ", self._handValue)
        i = 0
        while i < 2:
            i += 1
            self.split_hit(dealer, player_id)
        #self.main_hit(dealer, player_id)
        score1 = self._handValue
        print("Score: ",score1)


    def startingHand(self, dealer):
        """Calls the bet function once and the main_hit function twice to give the player
            his/hers starting hand"""
        
        self.bet(self._id)
        i = 0
        while i < 2:
            i += 1
            Hand(self._id)
            self.main_hit(dealer, self._id)
        self.main_hit(dealer, self._id)  

    def bet(self, player_id):
        """Sets the current players bet for the current hand"""
        i = 0
        while i < 1:
            bet = int(input("How much would player %s like to bet? " %player_id))
            if bet > self._balance:
               print("Insufficient funds! ")
            else:
               self._bet = bet
               i += 1
               print("Bet accepted! ")
        

    def hit(self):
        """This is called within both the dealers and players
           hit function, it gets the next card from the deck and does necessary
           checks in the case of drawing an ace"""
        
        temp = self._deck[0]
        new_card = temp
        if new_card._name[0] == "A" :
            if self._handValue >= 11 :
                new_card._cardValue = 1
            else:
                new_card._cardValue = 11
        self._deck.remove(self._deck[0])
        self._deck.append(temp)
        self._hand.add(new_card)
        self._handlst += [new_card]
        print(new_card)
        self._handValue += new_card._cardValue

    def countPlayerHand(self) :
        """add all the card values together to get the handvalue"""
        self._handValue = 0

        #iterate through the handlst and add each cards value toether
        for item in self._handlst :
            self._handValue += item._cardValue
        return self._handValue

    def bust(self, player_id, hand_value):
        """This is called in the case of the player going bust
            returns the players id."""
        
        #add the dictionary the hand value,bet andplayers balance for the player
        self._mainlst[player_id] = [hand_value, self._bet, self._balance]
        print("Player %s went bust \n" % (player_id))

    def stay(self, dealer, player_id, hand_value):
        """This is called when the player staying on a number
           this returns the players id and the number they stayed on"""

        #add the dictionary the hand value,bet andplayers balance for the player
        self._mainlst[player_id] = [hand_value, self._bet, self._balance]
        print(self._mainlst)
        print("Player %s stayed on Value = %i \n" % (player_id, hand_value))

    def compareHandAgainstDealer(self, dealer, mainlst) :
        """This is called when all players have either gone bust or stayed.
           Checks wether the players won or lost against the dealer.
           Updates each players balance accordingly."""

        print ( "Dealer Hand: %s" % ( dealer._hand))
        print ( "Dealer Score: %i\n" % (dealer._handValue))

        for item in mainlst :
            #check did the player bust
            if mainlst[item][0] > 21 :
                print ( "Player %i went Bust. Score: %i" % ( item, mainlst[item][0] ))
                mainlst[item][2] -= mainlst[item][1]
                print ( "Player %i Balance: %i \n" % ( item, mainlst[item][2]))
            #check did the dealer bust
            elif dealer._handValue > 21 :
                print ("Dealer Bust")
                print ("You win")
                (mainlst[item][2]) += (mainlst[item][1])
                print("Player %i Balance: %i\n" % (item,mainlst[item][2]))
            #check did the player beat the dealer
            elif mainlst[item][0] > dealer._handValue :
                print ( "Player %i Score: %i" % (item,mainlst[item][0]))
                print ( "You win\n" )
                (mainlst[item][2]) += (mainlst[item][1])
                print("Player %i Balance: %i\n" % (item,mainlst[item][2]))
            #check did the player draw with the dealer
            elif mainlst[item][0] == dealer._handValue :
                print ( "Draw, your bet has been refunded")
                print("Player %i Balance: %i\n" % (item,mainlst[item][2]))
            #check did the dealer beat the player
            else :
                print ( "Player %i Score: %i" % (item, mainlst[item][0]))
                print ("You Lose")
                mainlst[item][2] -= mainlst[item][1]
                print("Player %i Balance: %i\n" % (item, mainlst[item][2]))
