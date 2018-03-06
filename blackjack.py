from flask import Flask
from flask import render_template, redirect, url_for, session, request, flash, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from dealer import Dealer
from deck import Deck
from card import Card
from player import Player
from hand import Hand
#from blackjack import Actions
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '314159'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://sql2223630:aC2%mZ9%@sql2.freemysqlhosting.net/sql2223630"
db = SQLAlchemy(app)


class GamesTable(db.Model):
    __tablename__="GamesTable"
    gameID=db.Column('gameID',db.Integer,primary_key=True,nullable=False)
    numPlayers=db.Column('numPlayers',db.Integer, index=True, unique=False)
    activeID=db.relationship('ActiveUsers',backref='game',primaryjoin="GamesTable.gameID==ActiveUsers.gameID")
   
class ActiveUsers(db.Model):
    __tablename__="ActiveUsers"
    ID=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30), index=True, unique=True)
    gameID=db.Column(db.Integer,db.ForeignKey('GamesTable.gameID'),nullable=False)


class User(db.Model):
    __tablename__ = "registration_details"
    user_id = db.Column('ID',db.Integer , primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password', db.String(255))
    email = db.Column('email', db.String(255))
    balance = db.Column('balance', db.Integer)

class Actions(db.Model):
	__tablename__ = "Actions"
	actions_id = db.Column('ID', db.Integer, primary_key=True)
	action_name = db.Column('username', db.String(255))
	action_type = db.Column('type', db.String(255))
	action_game = db.Column('gameID', db.Integer)
	action_move = db.Column('action',db.String(255))
	action_hand = db.Column('hand', db.String(255))
	action_handValue = db.Column('handValue', db.Integer)
	action_stake = db.Column('stake',db.Integer)
	action_time = db.Column('action_time',db.DateTime)
#variables to be used 

playerCard1="" #players first card
playerCard2="" #players second card
playerCardHand = 0 #players hand value
dealerValue = 0 # dealers hand value
dealerCard="" #dealers first card
deck=[] # all remaining cards in deck
dv=0 #storage for dealers total value
pv=0 # storage for players total vlaue
count = 0
playerName = ''



@app.route('/')
#initail route
def blackjack():
	return render_template('blackjack.html')



@app.route('/gameinfo')
def getInfo():
	return('working')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/newGame')
#on new game button press
# intialise dealer and player
# assign all info to global variable to be used in future functions

#add sql
def newGame():
	dealer = Dealer()
	dealerdb= Actions(action_name="dealer",action_type="dealer",action_game=1,action_move="deal",action_hand=str(dealer._handlst[0])+","+str(dealer._handlst[1]),action_handValue=int(dealer._handValue),action_stake=0)
	db.session.add(dealerdb)
	db.session.commit()

	global dealerCard
	dealerCard = str(dealer._handlst[0]) # dealers first card
	global dealerValue
	dealerValue = int(dealer._handValue) # dealers total value
	global dv
	dv = dealerValue


	player = Player(dealer)
	player.startingHand(dealer)
	global playerName
	playerName = ActiveUsers.query.filter_by(ID=player._id).first()
	playerdb= Actions(action_name=playerName,action_type="player",action_game=1,action_move="deal",action_hand=str(player._handlst[0])+','+str(player._handlst[1]),action_handValue=int(dealer._handValue),action_stake=0)
	db.session.add(playerdb)
	db.session.commit()

	global playerCard1
	playerCard1 = str(player._handlst[0]) # players first card
	global playerCard2
	playerCard2= str(player._handlst[1]) # palyers second card
	global playerCardHand
	playerCardHand = int(player._handValue) # players total value
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
	Hand = Actions.query.filter_by(playerName),first()
	nextCard = deck[0]
	temp = str(deck[0])
	updatePlayerHand = Actions(action_name=playerName,action_type="player",action_game=1,action_move="hit",action_hand=Hand.action_hand+','+temp,action_value=Hand.action_handValue+nextCard._cardValue,action_stake=0)
	db.session.add(updatePlayerHand)
	db.session.commit()
	deck.remove(nextCard)
	nextCard=temp
	nextCard= json.dumps(nextCard)
	return(nextCard)

@app.route("/stay",methods=['POST'])
def stay():
	playNum = request.form['number']
	if playNum == 4:
		playerAct = Actions(action_name=playerName,action_type="player",action_game=1,action_move="stay")
		db.session.add(playerAct)
		db.session.commit()
		return('endgame')
	else:
		playerAct = Actions(action_name=playerName,action_type="player",action_game=1,action_move="stay")
		db.session.add(playerAct)
		db.session.commit()


@app.route('/getWinner')
# find out who won by compareing total hand values
def compareHands():
	global dv
	dv = dv
	global pv
	pv = pv
	print(pv)
	if dv > 21:
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='player wins')
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='dealer loses')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()
		return ("player wins dealer busts")
	elif(pv>21):
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='dealer wins')
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='playerloses')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()		
		return(" house wins player busts")
	elif(dv==pv):
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='draw')
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='draw')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()
		return ("Draw dealer and player have same total")

	elif(pv>dv):
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='player wins')
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='dealer loses')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()
		return("player wins")
	elif dv < pv:
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='player wins')
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='dealer loses')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()		
		return("player wins")
	else :
		dealerAct = Actions(action_name='dealer',action_type='dealer',actions_game=1,action_move='dealer wins')
		playerAct =Actions(action_name=playerName,action_type='Player',actions_game=1,action_move='player loses')
		db.session.add(playerAct)
		db.session.add(dealerAct)
		db.swession.commit()
		return ("dealer wins")

@app.route("/betting",methods = ['POST'])
#apply players bet
def bet():
	
	print(playerName)
	playerBet = request.form['myData']
	playerdb= Actions(action_name=playerName,action_type="player",action_game=1,action_move="bet",action_stake=playerBet)
	db.session.add(playerdb)
	db.session.commit()

	updateBal= User.query.filter_by(playerName)
	updateBal.balance -=playerbet
	db.session.commit()
	
	playerNum = request.form['player']
	return ('Player: '+playerNum + ' bets: '+ request.form['myData'])

@app.route("/updatePlayerInfo", methods=['POST'])
def updatePInfo():
	paid = request.form['paid']
	if paid:
		playerBal = User.query.filter_by(playerName)
		playerBal.balance+=request.form['amount']
		db.session.commit()


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
