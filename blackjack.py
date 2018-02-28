from flask import Flask, render_template,request,session,g,redirect,url_for,abort,flash,json
import random
from dealer import Dealer
from deck import Deck
from card import Card
from player import Player
from hand import Hand


app = Flask(__name__)
playerCard1="" #players first card
playerCard2="" #players second card
playerCardHand = 0 #players hand value
dealerValue = 0 # dealers hand value
dealerCard="" #dealers first card
deck=[] # all remaining cards in deck
dv=0 #storage for dealers total value
pv=0 # storage for players total vlaue


@app.route('/')
#initail route
def blackjack():
	return render_template('blackjack.html')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/newGame')
#on new game button press
# intialise dealer and player
# assign all info to global variable to be used in future functions

#add sql
def newGame():
	dealer = Dealer()
	global dealerCard
	dealerCard = str(dealer._handlst[0]) # dealers first card
	global dealerValue
	dealerValue = int(dealer._handValue) # dealers total value
	global dv
	dv = dealerValue
	player4 = Player(dealer)
	player4.startingHand(dealer)
	global playerCard1
	playerCard1 = str(player4._handlst[0]) # players first card
	global playerCard2
	playerCard2= str(player4._handlst[1]) # palyers second card
	global playerCardHand
	playerCardHand = int(player4._handValue) # players total value
	global pv
	pv= playerCardHand
	global deck
	deck = dealer._deck # store remaining cards
	print(str(deck[0]))
	return('hi new game started')

@app.route('/cardValue')
def cardValue():
	#convert dealers card to a json object and return to javascript
	global dealerCard
	dealerCard = json.dumps(dealerCard)
	return(dealerCard)

@app.route('/playerCardValue1')
def playerCard1():
	#convert players card to a json object and return to javascript
	global playerCard1
	playerCard1 = json.dumps(playerCard1)
	return(playerCard1)

@app.route('/playerCardValue2')
def playerCard2():	
	#convertplayers card to a json object and return to javascript
	global playerCard2
	playerCard2 = json.dumps(playerCard2)
	return(playerCard2)

@app.route('/handValue',methods = ['POST'])
def getPlayerHandValue():
	#update players hand value convert to json object
	cardValue = request.form['cardValue']
	cardValue=int(cardValue)
	global pv
	pv+=cardValue
	global playerCardHand
	playerCardHand += cardValue
	playerCardHand = json.dumps(playerCardHand)
	return(playerCardHand)

@app.route('/dealerValue')
def getDealerValue():
	# returns dealers total value
	global dealerValue
	dealerValue = json.dumps(dealerValue)
	return (dealerValue)

##add sql
@app.route("/hit")
def getNewCard():
	#get new card byremoving and updating deck
	global deck
	nextCard = deck[0]
	temp = str(deck[0])
	deck.remove(nextCard)
	nextCard=temp
	nextCard= json.dumps(nextCard)
	return(nextCard)


@app.route('/getWinner')
# find out who won by compareing total hand values
def compareHands():
	global dv
	dv = dv
	global pv
	pv = pv
	print(pv)
	if dv > 21:
		return ("player wins dealer busts")
	elif(dv==pv):
		return ("Draw dealer and player have same total")
	elif(pv>21):
		return(" house wins player busts")
	elif(pv>dv):
		return("player wins")
	elif dv < pv:
		return("player wins")
	elif dv ==21:
		return ("dealer wins")
	else :
		return ("dealer wins")

@app.route("/betting",methods = ['POST'])
#apply players bet
def bet():
	playerNum = request.form['player']
	print(playerNum)
	return ('Player: '+playerNum + ' bets: '+ request.form['myData'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

@app.route("/newHand")
@app.route("/Hit2")
@app.route("/newGame2")
@app.route("/stay")
@app.route("/dealer")
@app.route("/leavegame")
@app.route("/logout")
@app.route("/register")
@app.route("/login")

"""
if __name__ == '__main__':
	app.run(debug=True)
