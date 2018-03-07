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
from dealer import Dealer
from deck import Deck
import datetime

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


class User(UserMixin, db.Model):
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


class GamesTable(Base, db.Model):
    __tablename__="GamesTable"
    gameID=db.Column(db.Integer,db.ForeignKey('ActiveUsers.gameID'),primary_key=True,nullable=False,autoincrement=True)
    NumPlayers=db.Column(db.Integer, index=True, unique=False)
    activeUsers = db.relationship("ActiveUsers", backref="GamesTable")



    def __init__(self,NumPlayers):
        self.NumPlayers = NumPlayers

class Actions(Base,db.Model):
	__tablename__ = "Actions"
	action_id = db.Column('ID', db.Integer, primary_key=True)
	action_name = db.Column('username', db.String(255))
	action_type = db.Column('type', db.String(255))
	action_game = db.Column('gameID', db.Integer)
	action_move = db.Column('action',db.String(255))
	action_hand = db.Column('hand', db.String(255))
	action_handValue = db.Column('handValue', db.Integer)
	action_stake = db.Column('stake',db.Integer)
	action_time = db.Column('action_time',db.DateTime,default=datetime.datetime.utcnow)

	def __init__(self,action_id,action_name,action_type,actions_game,action_move,action_hand,action_handValue,action_stake,action_time):
		self.id = action_id
		self.username = action_name
		self.type = action_type
		self.gameID = action_game
		self.move = action_move
		self.hand = action_hand
		self.handvalue = action_handValue
		self.stake = action_stake
		self.timestamp = action_time

class Seat(Base,db.Model):
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



class Deck(Base,db.Model):
	__tablename__="Deck"
	deck_id = db.Column("ID",db.Integer,primary_key=True)
	card = db.Column("card",db.String(255))
	gameID = db.column("gameID",db.String(255))


	def __init__(self,card,gameID):
		self.card = card
		self.gameID = gameID




class ActiveUsers(Base, db.Model):
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

@app.route('/waiting', methods=['GET', 'POST'])
@login_required
def waiting(): 
    return render_template("waiting.html")

@app.route('/newhand',methods=['GET','POST'])
def newhand():
	hand_count = 0
	handScore = 0
	hand = ""
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	global deck
	clear_deck = Deck.query.filter_by(gameID=gameID)
	db.session.delete(clear_deck)
	db.session.commit()
	
	while hand_count < 2:
		nextcard = str(deck[0])
		cardsplayed = Deck.query.filter_by(gameID=gameID).all()
		
		if nextcard not in cardsplayed:
			handScore += deck[0]._cardValue
			newcard = Deck(card=nextcard,gameID=gameID)
			db.session.add(newcard)
			db.session.commit()
			hand_count += 1
			deck.remove(deck[0])
			hand += "," + nextcard
		else:
			deck.remove(deck[0])

	#get the line of dealer
	dealer_go = Actions.query.filter_by(type="dealer",gameID=game.gameID)
	current_time = datetime.datetime.now().time()
	diff_time = dealer.timestamp - current_time
	if diff_time < 3000: #gamelength
		dealer = Dealer()
		dealer_go.hand = dealer._handlst
		dealer_go.handValue = dealer._handValue
		dealer._go.timestamp = datetime.datetime.now().time()
		db.session.commit()
	#check if time is more than gamelength older that current time
	#if it is deal away mad
	#other wise pass

	
	updatePlayerHand = Actions(action_name=playerName,action_type="player",action_game=gameID,action_move="new_hand",action_hand=hand,action_value=handScore,action_stake=0)
	db.session.add(updatePlayerHand)
	db.session.commit()
	nextCard= json.dumps(deck[0])
	return (handScore)



@app.route("/hit")
def getNewCard():
	#get new card by removing and updating deck
	switch = True
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	global deck
	cardsplayed = Deck.query.filter_by(gameID=gameID).all()
	Hand = Actions.query.filter_by(username=playerName).first()
	nextCard = str(deck[0])
	Hand.handValue += deck[0]._cardValue
	while switch:
		if nextcard not in cardsplayed:
			newcard = Deck(nextcard,gameID)
			db.session.add(newcard)
			db.session.commit()
			Hand.hand += nextcard
			switch = False
			if deck[0]._name[0] == "A":
				if action._handValue >= 11:
					nextCard._cardValue = 1
				else:
					for item in Hand.action_hand :
						if item[0] == "A" :
							if action._handValue >= 11:
								item._cardValue = 1
		else:
			deck.remove(deck[0])
			nextCard = str(deck[0])


	updatePlayerHand = Actions(action_name=playerName,action_type="player",action_game=gameID,action_move="hit",action_hand=Hand.hand,action_value=Hand.handValue,action_stake=0)
	db.session.add(updatePlayerHand)
	db.session.commit()
	deck.remove(deck[0])
	nextCard= json.dumps(deck[0])
	return(nextCard)

@app.route("/betting",methods = ['POST'])
#apply players bet
def bet():
	playerBet=request.json['bet']
	print(playerBet)
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	username = session['username']
	playerdb= Actions(action_name=username,action_type="player",action_game=gameID,action_move="bet",action_stake=playerBet)
	db.session.add(playerdb)
	db.session.commit()

	updateBal= User.query.filter_by(username=playerName)
	updateBal.balance -= playerBet
	db.session.commit()
	
	playerNum = request.form['player']
	return (updateBal.balance)

@app.route("/stay",methods=['POST'])
def stay():
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	game = GamesTable.query.filter_by(gameID=gameID)
	if playNum == 4:
		playerAct = Actions(action_name=playerName,action_type="player",action_game=gameID,action_move="stay")
		db.session.add(playerAct)
		db.session.commit()
		return('endgame')
	else:
		playerAct = Actions(action_name=playerName,action_type="player",action_game=gameID,action_move="stay")
		db.session.add(playerAct)
		db.session.commit()

@app.route('/register', methods=['GET', 'POST'])

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
	#activeuser = ActiveUsers.query(ActiveUsers.username).all()
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

@app.route('/gameinfo')
def getInfo():

	currentAction = Actions.query.filter_by(timestamp=db.func.max(Actions.action_time))
	if currentAction.action_move == 'deal':
		#get currentAction.action_name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction._username).first()
		seatnum = player.SeatNum
		#sc handsplit splits the hand into strings for each card e.g "80fHearts"
		handsplit = currentAction.action_hand.split(",")
		#sc Returns the first 2 cards in players hand along with seat number and handvalue
		return({'hand1':handsplit[0],'hand2':handsplit[1],'seatnum':seatnum,'value':currentAction_handValue})
	elif currentAction.action_move == 'bet':
		#get currentAction.action_name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction._username).first()
		seatnum = player.SeatNum
		return({'bet':currentAction.action_hand,'seatnum':seatnum})
	elif currentAction.action_move == 'hit':
		#get currentAction.action_name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction._username).first()
		seatnum = player.SeatNum
		#split the hand from hit and return the most recent card dealt
		#sc handsplit returns a list of strings that are the names of the players cards
		handsplit = currentAction.action_hand.split(",")
		#sc this for loop runs through the list of strings to find the last card added
		count = -1
		for item in handsplit :
			count += 1
		    #sc this then returns the last card, seat number and handvalue
		return({'hand3':handsplit[count],'seatnum':seatnum,'value':currentAction_handValue})
	elif currentAction.action_move == 'stay':
		#get currentAction.acion_name's seat number
		#sc player queries SeatsTable for seat number using their username as key
		player = SeatsTable.query.filter_by(username=currentAction._username).first()
		seatnum = player.SeatNum
		return({'seatnum':seatnum,'value':currentAction_handValue})
	# return if each player wins or loses does it really matter?
	return('working')

@app.route('/joingame', methods=['GET','POST'])
def joingame():
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

	return render_template("blackjack.html", username=username, seatnum=seatnum)




@app.route('/lobby',methods=['GET','POST'])  
 
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

@app.route('/getWinner',methods = ['GET','POST'])
 # find out who won by comparing total hand values
def compareHands():
	username = session['username']
	game = ActiveUsers.query.filter_by(username=username).first()
	gameID = game.gameID
	player = Actions.query.filter_by(action_name=username,action_move='bet').first()
	winnings = (player.stake)*2
	user = User.query.filter_by(username=username)

 	player = Actions.query.filter_by(username=username,gameId=gameID).first()
 	dealer1 = Actions.query.filter_by(type='dealer',gameID=gameID).first()
 	pv = player.handvalue 
 	dv = dealer1.handvalue
	 	
 	if dv > 21:
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='win')
		db.session.add(playerAct)
		db.session.commit()
		user.balance += winnings
		db.session.commit()
 		return ("You win!")
	elif(dv==pv):
		return ("Draw!")
 	elif(pv>21):
		
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='lost')
		db.session.add(playerAct)
		db.session.commit()
		
 		return("Dealer Wins!")
	elif(dv==pv):
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='draw')
		
		db.session.add(playerAct)
		db.session.commit()
		user.balance += (winnings/2)
		db.session.commit()
		return ("Draw!")
	elif(pv>dv):
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='win')
		
		db.session.add(playerAct)
		db.session.commit()
		
 		return("You win!")
 	elif dv < pv:
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='win')
		db.session.add(playerAct)
		db.session.commit()	
		user.balance += winnings
		db.session.commit()
 		return("You win!")
	elif dv ==21:
		return ("dealer wins!")
	else :
		playerAct =Actions(action_name=username,action_type='Player',actions_game=gameID,action_move='lost')
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


if __name__ == '__main__':
    
    app.run(debug=True)