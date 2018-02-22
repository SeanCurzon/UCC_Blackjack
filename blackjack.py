from flask import Flask, render_template,request,session,g,redirect,url_for,abort,flash,json
import random
from dealer import Dealer
from deck import Deck
from card import Card
from player import Player
from hand import Hand


app = Flask(__name__)
playerlst = []
dealerCard=""
@app.route('/')
def blackjack():
	#player4.compareHandAgainstDealer(dealer, player4._mainlst)
	return render_template('blackjack.html')

@app.route('/newGame')
def newGame():
	dealer = Dealer()
	global dealerCard
	dealerCard = str(dealer._handlst[0])
	player1 = Player(dealer)
	player2 = Player(dealer)
	player3 = Player(dealer)
	player4 = Player(dealer)
	global playerlst
	playerlst = [player1,player2,player3,player4]
	return('hi')

@app.route('/cardValue')
def cardValue():
	global dealerCard
	dealerCard = json.dumps(dealerCard)
	return(dealerCard)


@app.route("/betting",methods = ['POST'])
#apply players bet incomplete
def bet():
	playerNum = request.form['player']
	print(playerNum)
	return ('Player: '+playerNum + ' bets:'+ request.form['myData'])

	#return(request.form['myData'])

if __name__ == '__main__':
	app.run(debug=True)
