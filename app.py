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

Base = declarative_base()

app = Flask(__name__)
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
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('dashboard'))

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
    return render_template('dashboard.html', name=current_user.username,gamesList=gamesList)

@app.route('/createGame', methods=['GET', 'POST'])
@login_required
def createGame():

    game = GamesTable(NumPlayers = 1)
    db.session.add(game)
    db.session.commit()
    activeUsers = ActiveUsers()
    activeUsers.gameID = game.gameID
    db.session.add(activeUsers)
    db.session.commit()

    return redirect(url_for('dashboard'))  

@app.route('/showgame')    
def showgame():
    return render_template('blackjack.html')  

@app.route('/logout') #logs out the current user
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True)
