#!/bin/env python
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_table import Table, Col, LinkCol
from sqlalchemy.ext.declarative import declarative_base
from time import gmtime, strftime
#from dealer import Dealer
#from deck import Deck
import datetime
import random
	

Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql2223630:aC2%mZ9%@sql2.freemysqlhosting.net/sql2223630'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Following Class's are python representation of our different tables in our Database
#Required to make changes in Flask to any table

class User(UserMixin, db.Model): #Registration Details Table class structure
    __tablename__ = "registration_details"
    user_id = db.Column('ID',db.Integer , primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password', db.String(255))
    email = db.Column('email', db.String(255))
    balance = db.Column('balance', db.Integer)

    def __init__(self, user_id, username ,password, email, balance): 
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.balance = balance

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class GamesTable(Base, db.Model): #Games Table class structure
    __tablename__="GamesTable"
    gameID=db.Column(db.Integer,db.ForeignKey('ActiveUsers.gameID'),primary_key=True,nullable=False,autoincrement=True)
    NumPlayers=db.Column(db.Integer, index=True, unique=False)
    activeUsers = db.relationship("ActiveUsers", backref="GamesTable")



    def __init__(self,NumPlayers):
        self.NumPlayers = NumPlayers

class Actions(Base,db.Model): ##Actions Table class structure
	__tablename__ = "Actions"
	id = db.Column('ID', db.Integer, primary_key=True,autoincrement=True)
	username = db.Column('username', db.String(255))
	types = db.Column('type', db.String(255))
	gameID = db.Column('gameID', db.Integer)
	move = db.Column('action',db.String(255))
	hand = db.Column('hand', db.String(255))
	handValue = db.Column('handValue', db.Integer)
	stake = db.Column('stake',db.Integer)
	time = db.Column('action_time',db.DateTime,default=datetime.datetime.utcnow)

	def __init__(self,username,types,gameID,move,hand,handValue,stake):
		
		self.username = username
		self.types = types
		self.gameID = gameID
		self.move = move
		self.hand = hand
		self.handValue = handValue
		self.stake = stake
		

class Seat(Base,db.Model): ##Seats Table class structure
	__tablename__="SeatsTable"
	seat_id = db.Column("ID",db.Integer,primary_key=True)
	username = db.Column("username",db.String(255))
	gameID = db.Column("GameID",db.Integer)
	seatNum = db.Column("SeatNum",db.Integer)
	timestamp = db.Column("timestamp",db.DateTime,default=datetime.datetime.utcnow)

	def __init__(self,username,gameID,seatNum):
		self.username = username
		self.gameID = gameID
		self.seatNum = seatNum



class Deck(Base,db.Model): #Deck Table class structure
	__tablename__="Deck"
	deck_id = db.Column("ID",db.Integer,primary_key=True)
	card = db.Column("card",db.String(255))
	gameID = db.column("gameID",db.String(255))


	def __init__(self,card,gameID):
		self.card = card
		self.gameID = gameID




class ActiveUsers(Base, db.Model): ##Active Users Table class structure
    __tablename__="ActiveUsers"
    ID=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30), index=True, unique=True)
    gameID=db.Column(db.Integer,nullable=False)


    def __init__(self):
        self.username = current_user.username



class LoginForm(FlaskForm): #define login form for bootstrap
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm): #define registration form for bootstrap
    email = StringField('email', validators=[InputRequired(), Length(max=50), Email("This field requires a valid email address")])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class Lobby(Table):
    gameId=Col('ID')
    count=Col('Number of Players')
    users=Col('users')
    

    def __init__(self, gameID, numPlayers):
       self.gameID = gameID
       self.numPlayers = numPlayers



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/') #index page
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) #login page
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    username = form.username.data
    password = form.password.data
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    session['username'] = username
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('lobby'))

@app.route('/waiting', methods=['GET', 'POST']) #Endpoint to allow for player to join current game
@login_required
def waiting(): 
    return render_template("waiting.html")

@app.route('/newhand',methods=['GET','POST']) #End point creates a new hand in the game
def newhand():

	#Could not import and classes from other files so had to implement 
	#Deck class statically.
	i=0
	deck = []
	faces = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
	suits = ['Diamonds','Clubs','Hearts','Spades']
	while i < 1:
	    i += 1
	    for f in range(len(faces)):
	        for s in range(len(suits)):
	        	if faces[f] in ['10','J','Q','K']:
	        		deck.append([faces[f] + "of" + suits[s],10])
	        	elif faces[f] == 'A':
	        		deck.append([faces[f] + "of" + suits[s], 11])
	        	else:
	        		deck.append([faces[f] + "of" + suits[s], int(faces[f])])
	random.shuffle(deck)
	hand_count = 0
	handScore = 0
	dealerScore=0
	dealerhand=""
	hand = ""
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	deck
	clear_deck = Deck.query.get(gameID) #clear deck table to allow allocation of cards for new hand

	if clear_deck:
		print(clear_deck)
		db.session.delete(clear_deck)
		db.session.commit()
	
	while hand_count < 2: #deal out 2 cards tro player and store in relevant tables
		nextcard = str(deck[0])
		cardsplayed = Deck.query.filter_by(gameID=gameID).all()
		
		if nextcard not in cardsplayed:
			handScore += deck[0][1]
			newcard = Deck(card=nextcard,gameID=gameID)
			db.session.add(newcard)
			db.session.commit()
			hand_count += 1
			deck.remove(deck[0])
			hand = deck[0][0]+','
		else:
			deck.remove(deck[0])

	playerAction = Actions(username="dealer",types="dealer",gameID=gameID,move="newhand",hand=dealerhand,handValue=dealerScore,stake=0)
	db.session.add(playerAction)
	db.session.commit()
	dealer_go = Actions.query.filter_by(types="dealer",gameID=gameID)
	#deal cards for dealer and store in table
	if dealer_go:
		current_time = datetime.datetime.now().time()
		i=0
		while i < 2:
			 #gamelength
			dealerhand += deck[0][0]+','
			dealerScore += deck[0][1]
			i+=1
		dealer_go.hand = dealerhand
		dealer_go.handValue = dealerScore
		dealer_go.timestamp = datetime.datetime.now().time()
		db.session.commit()
		
	#check if time is more than gamelength older that current time

	#id,name,type,game,move,hand,handValue,stake,time
	playerAction = Actions(username=playerName,types="player",gameID=gameID,move="newhand",hand=hand,handValue=handScore,stake=0)
	
	db.session.add(playerAction)
	db.session.commit()
	
	
	return (str(handScore))



@app.route("/hit") #deals out next card for player and 
def getNewCard():
	#had to statically implement Deck class again
	i=0
	deck = []
	faces = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
	suits = ['Diamonds','Clubs','Hearts','Spades']
	while i < 1:
	    i += 1
	    for f in range(len(faces)):
	        for s in range(len(suits)):
	        	if faces[f] in ['10','J','Q','K']:
	        		deck.append([faces[f] + "of" + suits[s],10])
	        	elif faces[f] == 'A':
	        		deck.append([faces[f] + "of" + suits[s], 11])
	        	else:
	        		deck.append([faces[f] + "of" + suits[s], int(faces[f])])
	random.shuffle(deck)
	switch = True
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	cardsplayed = Deck.query.filter_by(gameID=gameID).all()
	Hand = Actions.query.filter_by(username=playerName).first()
	nextCard = str(deck[0])
	Hand.handValue += deck[0][1]
	while switch:
		#This checks deck class to see if card from deck has been handed out already.
		if nextCard not in cardsplayed:
			newcard = Deck(nextCard,gameID)
			db.session.add(newcard)
			db.session.commit()
			Hand.hand += nextCard
			switch = False
			if deck[0][0] == "A":
				if action.handValue >= 11:
					nextCard[1] = 1
				else:
					for item in Hand.hand:
						if item[0][0] == "A" :
							if action._handValue >= 11:
								item[1] = 1
		else:
			deck.remove(deck[0])
			nextCard = str(deck[0])


	updatePlayerHand = Actions(username=playerName,types="player",gameID=gameID,move="hit",hand=Hand.hand,handValue=Hand.handValue,stake=0)
	db.session.add(updatePlayerHand)
	db.session.commit()
	deck.remove(deck[0])
	
	return(str(deck[0][0]))

@app.route("/bet",methods = ['POST']) #adds player bet from Ajax request, validates and inserts into Actions table
#apply players bet
def bet():
	username = session['username']
	playerBet=request.form['bet']
	print(playerBet)
	whichGame = ActiveUsers.query.filter_by(username=username).first()
	gameID = whichGame.gameID
	playerdb= Actions(username=username,types="player",gameID=gameID,move="bet",hand="",handValue=0,stake=playerBet)
	db.session.add(playerdb)
	db.session.commit()

	updateBal= User.query.filter_by(username=username).first()
	print(updateBal)
	balance = int(updateBal.balance)
	balance -= int(playerBet)
	updateBal.balance = balance
	db.session.commit()
	
	
	return (str(balance))

@app.route("/stay",methods=['POST']) #endshand for player.
def stay():
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	game = GamesTable.query.filter_by(gameID=gameID).first()
	playNum = game.NumPlayers
	if playNum == 4:
		playerAct = Actions(username=playerName,types="dealer",gameID=gameID,move="end_of_hand",hand="",handValue=0,stake=0)
		db.session.add(playerAct)
		db.session.commit()
		return('endgame')
	else:
		playerAct = Actions(username=playerName,types="player",gameID=gameID,move="stay",hand="",handValue=0,stake=0)
		db.session.add(playerAct)
		db.session.commit()
		finalcardvalue = Actions.query.filter_by(username=playerName,move="hit").first()


	return(str(finalcardvalue.handValue))

@app.route('/register', methods=['GET', 'POST']) #registers player into register details table

def signup():

    form = RegisterForm()

    username = form.username.data #collects data from registration form
    password = form.password.data
    email = form.email.data
    balance = 1000

    if form.validate_on_submit():
        if request.method == 'GET':
            return render_template('register.html')
        user = User(0, username , password, email, balance)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    games=GamesTable.query.all()
    gamesList = GamesTable.query.join(ActiveUsers, GamesTable.gameID==ActiveUsers.gameID).add_columns(GamesTable.gameID, GamesTable.NumPlayers).filter(GamesTable.gameID == ActiveUsers.gameID)
    return render_template('blackjack.html', name=current_user.username,gamesList=gamesList)

@app.route('/createGame', methods=['GET', 'POST'])
@login_required
def createGame(): #create new instance of game and insert game into games table and user into active users
	
	username=session['username']
	activeusers = db.session.query(ActiveUsers.username).all()
	checker = ActiveUsers.query.filter_by(username=username)
	balance = db.session.query(User).filter_by(username=username).first()
	if checker:
		print("already there biy")
		print(balance)
		return render_template("blackjack.html", username=username,balance=balance)
	else:
		username = session['username']
		balance = db.session.query(User.balance).filter_by(username=username).first()
		print(user)
		game = GamesTable(NumPlayers = 1) #not sure if gameid can be called after this. possibly need select statement to activeusers
		db.session.add(game)
		db.session.commit()
		activeUsers = ActiveUsers()
		activeUsers.username = username
		activeUsers.gameID = game.gameID
		db.session.add(activeUsers)
		db.session.commit()
		seat = Seat(username=username,gameID=game.gameID,seatNum=1)
		db.session.add(seat)
		db.session.commit()
	
		return render_template("blackjack.html" ,balance=balance) 

"""@app.route('/gameinfo')#to implemnt as multiplayer solution. checks actions table every second to update js client.
def getInfo():
	username=session['username']
	
	currentAction =db.session.query(Actions).filter_by(name=username).first()
	print(currentAction.move)
	if currentAction.move == 'deal':
		#get currentAction.name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = Seat.query.filter_by(username=currentAction.name).first()
		seatnum = player.SeatNum
		#sc handsplit splits the hand into strings for each card e.g "80fHearts"
		handsplit = currentAction.hand.split(",")
		#sc Returns the first 2 cards in players hand along with seat number and handvalue
		return({'hand1':handsplit[0],'hand2':handsplit[1],'seatnum':seatnum,'value':currentAction.handValue})
	elif currentAction.move == 'bet':
		#get currentAction.name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction.username).first()
		seatnum = player.SeatNum
		return({'bet':currentAction.hand,'seatnum':seatnum})
	elif currentAction.move == 'hit':
		#get currentAction.name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction.username).first()
		seatnum = player.SeatNum
		#split the hand from hit and return the most recent card dealt
		#sc handsplit returns a list of strings that are the names of the players cards
		handsplit = currentAction.hand.split(",")
		#sc this for loop runs through the list of strings to find the last card added
		count = -1
		for item in handsplit :
			count += 1
		    #sc this then returns the last card, seat number and handvalue
		return({'hand3':handsplit[count],'seatnum':seatnum,'value':currentAction.handValue})
	elif currentAction.move == 'stay':
		#get currentAction.acion_name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction.username).first()
		seatnum = player.SeatNum
		return({'seatnum':seatnum,'value':currentAction.handValue})
	# return if each player wins or loses does it really matter?
	return('working')
"""
@app.route('/joinGame', methods=['GET','POST'])#allows players to join game
@login_required
def joinGame():
    gameID = request.args.get('gameID')
    correctPath = False
    if Actions.query.filter_by(types="dealer",move="end_of_hand", gameID=gameID).first(): 
        correctPath = True
        return redirect(url_for("waiting", gameID=gameID, correctPath=correctPath))

@app.route('/showgame', methods=['GET','POST'])#allows players to join game
def showgame():
	username = session['username']
	gameID = request.args.get('gameID')
	seatslist = Seat.query.filter_by(gameID=gameID).all()
	for i in range(len(seatlist)-1):
		if i not in seatlist:
			playerSeat = Seat(username=username,gameID=gameID,seatNum=i)
	game= GamesTable.query.filter_by(gameID)
	game.numPlayers += 1
	db.session.commit()
	player = ActiveUsers(username=username,gameID=gameID)
	db.session.add(player)
	db.session.commit()
	return render_template("blackjack.html")




@app.route('/lobby',methods=['GET','POST'])  #populates a lobby of all games currently active
 
def lobby():
    usersDict={}
    gamesDict={}
    gameplayers=db.session.query(ActiveUsers.username,ActiveUsers.gameID).all()
    for tuples in gameplayers:
        if str(tuples[1]) not in usersDict:
            usersDict[str(tuples[1])]=[str(tuples[0])]
        else:
            usersDict[str(tuples[1])]+=[str(tuples[0])]
    print(usersDict)

    gamelist = db.session.query(GamesTable.gameID,GamesTable.NumPlayers).all()
    print(gamelist)
    for tuples in gamelist:
        if str(tuples[0]) not in gamesDict:
            gamesDict[str(tuples[0])]=str(tuples[1])
        
    print(gamesDict)


    return render_template('lobby.html',gamesDict=gamesDict, usersDict=usersDict)

@app.route('/getWinner',methods = ['GET','POST']) # checks if player is winner and updates balance accordingly
 # find out who won by comparing total hand values
def compareHands():
	username = session['username']
	game = ActiveUsers.query.filter_by(username=username).first()
	gameID = game.gameID
	player = Actions.query.filter_by(username=username,move='bet').first()
	winnings = (player.stake)*2
	user = User.query.filter_by(username=username)
	player = Actions.query.filter_by(username=username,gameID=gameID).first()
	dealer1 = Actions.query.filter_by(types='dealer',gameID=gameID).first()
	pv = player.handValue 
	dv = dealer1.handValue
	if dv > 21:
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='win')
		db.session.add(playerAct)
		db.session.commit()
		user.balance += winnings
		db.session.commit()
		return ("You win!")
	elif(dv==pv):
		return ("Draw!")
	elif(pv>21):
		
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='bust',hand="",handValue=0,stake=0)
		db.session.add(playerAct)
		db.session.commit()
		return("Dealer Wins!")
	elif(dv==pv):
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='draw',hand="",handValue=0,stake=0)
		
		db.session.add(playerAct)
		db.session.commit()
		user.balance += (winnings/2)
		db.session.commit()
		return ("Draw!")
	elif(pv>dv):
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='win',hand="",handValue=0,stake=0)
		
		db.session.add(playerAct)
		db.session.commit()
		return("You win!")
	elif dv < pv:
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='win',hand="",handValue=0,stake=0)
		db.session.add(playerAct)
		db.session.commit()	
		user.balance += winnings
		db.session.commit()
		return("You win!")
	elif dv ==21:
		return ("dealer wins!")
	else :
		playerAct =Actions(username=username,types='Player',gameID=gameID,move='lost',hand="",handValue=0,stake=0)
		db.session.add(playerAct)
		db.swession.commit()
	return ("endhand")

@app.route('/logout') #logs out the current user
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/leavegame')
def leaveGame():
	username = session['username']
	active_me = ActiveUsers.query.filter_by(username=username).first()
	gameID = active_me.gameID
	db.session.delete(active_me)
	db.session.commit()

	#activeusers
	game = GamesTable.query.filter_by(gameID = gameID)
	game.numPlayers -= 1
	#gemas table reduced numPlayers
	#update seatstab
	seat_me = Seat.query.filter_by(username=username)
	db.session.delete(seat_me)
	db.session.commit()
	#remove from chattable
	chat_me = Chat.query.filter_by(username=username)
	db.session.delete(chat_me)
	db.session.commit()

	return render_template('lobby.html',gamesDict=gamesDict, usersDict=usersDict)
@app.route('/cardValue')
def cardValue():

	#convert dealers card to a json object and return to javascript
	dealerCard = Actions.query.filter_by(username ='dealer').first()
	tempHand = dealerCard.hand.split(",")
	dealerCard = tempHand[0]
	
	return(dealerCard)

@app.route('/playerCardValue1') #returns player card to show in JS
def playerCard1():
	username = session['username']
	#convert players card to a json object and return to javascript
	#insert session[username] here i think?
	playerCard1 = Actions.query.filter_by(username = username).first()
	tempHand = playerCard1.hand.split(",")
	playerCard1 = tempHand[0]
	return(playerCard1)

@app.route('/playerCardValue2') #returns player card to show in JS
def playerCard2():	
	username = session['username']
	#convertplayers card to a json object and return to javascript
	#insert session[username] here i think?
	playerCard2 = Actions.query.filter_by(username = username).first()
	tempHand = playerCard2.hand.split(",")
	playerCard2 = tempHand[0]
	return(playerCard2)

@app.route('/handValue',methods = ['POST']) #gets handvalue of player
def getPlayerHandValue():
	#update players hand value convert to json object
	cardValue = request.form['cardValue']
	#call ace checker function will be put in later by sean to fix ace bug
	cardValue=int(cardValue)
	playerHandValue
	playerHandValue= Actions.query.filter_by(types= "player").first()
	playerHandValue = playerHandValue.handValue + cardValue


	return(str(playerHandValue))

@app.route('/dealerValue') #gets dealer handvalue
def getDealerValue():
	# returns dealers total value
	dealerValue = Actions.query.filter_by(move="deal").first()
	dealerValue = dealerValue.handValue # dealers total value
	return (str(dealerValue))


if __name__ == '__main__':
    
    app.run(debug=True)