from flask import Flask, render_template,request,session,g,redirect,url_for,abort,flash,json
import random
from dealer import Dealer
from deck import Deck
from card import Card
from player import Player
from hand import Hand


app = Flask(__name__)
playerCard1=""
playerCard2=""
playerCardHand = 0
dealerValue = 0
dealerCard=""
dv=0
pv=0
@app.route('/')
def blackjack():
	#player4.compareHandAgainstDealer(dealer, player4._mainlst)

	return render_template('blackjack.html')

@app.route('/newGame')
def newGame():
	dealer = Dealer()
	global dealerCard
	dealerCard = str(dealer._handlst[0])
	global dealerValue
	dealerValue = int(dealer._handValue)
	global dv
	dv = dealerValue
	player4 = Player(dealer)
	player4.startingHand(dealer)
	global playerCard1
	playerCard1 = str(player4._handlst[0])
	global playerCard2
	playerCard2= str(player4._handlst[1])
	global playerCardHand
	playerCardHand = int(player4._handValue)
	global pv
	pv= playerCardHand
	return('hi new game started')

@app.route('/cardValue')
def cardValue():
	global dealerCard
	dealerCard = json.dumps(dealerCard)
	return(dealerCard)

@app.route('/playerCardValue1')
def playerCard1():
	global playerCard1
	playerCard1 = json.dumps(playerCard1)
	return(playerCard1)

@app.route('/playerCardValue2')
def playerCard2():	
	global playerCard2
	playerCard2 = json.dumps(playerCard2)
	return(playerCard2)

@app.route('/handValue')
def getPlayerHandValue():
	global playerCardHand
	playerCardHand = json.dumps(playerCardHand)
	return(playerCardHand)

@app.route('/dealerValue')
def getDealerValue():
	global dealerValue
	dealerValue = json.dumps(dealerValue)
	return (dealerValue)

@app.route('/getWinner')
def compareHands():
	global dv
	dv = dv
	global pv
	pv = pv
	print(dv>21)
	if dv > 21:
		return ("player wins dealer busts")
	elif dv < pv:
		return("player wins")
	elif(dv==pv):
		return ("Draw dealer and player have same total")
	elif(pv>21):
		return(" house wins player busts")
	elif(pv>dv):
		return("player wins")
	elif dv ==21:
		return ("dealer wins")
	else :
		return ("dealer wins")
@app.route("/betting",methods = ['POST'])
#apply players bet incomplete
def bet():
	playerNum = request.form['player']
	print(playerNum)
	return ('Player: '+playerNum + ' bets: '+ request.form['myData'])

	#return(request.form['myData'])

if __name__ == '__main__':
	app.run(debug=True)
