#!/bin/env python
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from time import gmtime, strftime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/mysql'#'mysql://sql2223630:aC2%mZ9%@sql2.freemysqlhosting.net/sql2223630'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = "users"
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

class Chat(db.Model):
    __tablename__ = "chat"
    message_id = db.Column('ID',db.Integer , primary_key=True)
    gameID = db.Column('gameID', db.Integer)
    username = db.Column('username', db.String(255))
    message = db.Column('message', db.String(255))
    timestamp = db.Column('timestamp', db.String(255))

    def __init__(self, message_id, gameID, username ,message, timestamp):
        self.message_id = message_id
        self.gameID = gameID
        self.username = username
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return "<Username: {} - Message: {}>".format(self.username, self.message)

class ChatForm(FlaskForm): #define login form for bootstrap
    message = StringField('message', validators=[InputRequired()])

class LoginForm(FlaskForm): #define login form for bootstrap
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm): #define registration form for bootstrap
    email = StringField('email', validators=[InputRequired(), Length(max=50), Email("This field requires a valid email address")])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/') #index page
def index():
    return render_template('index.html')

@app.route('/blackjack', methods=['GET', 'POST']) #index page
def blackjack():

    form  = ChatForm()
    comments = Chat.query.order_by(Chat.message_id.desc())

    name = current_user.username
    message = form.message.data
    timestamp = strftime(" %H:%M - %d %b %Y", gmtime())

    if form.validate_on_submit():
        if request.method == 'GET':
            return render_template('blackjack.html')
        comment = Chat(0, 1, name, message, timestamp)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blackjack'))
    return render_template('blackjack.html', form=form, name=current_user.username, comments=comments)

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
        user = User(0, username, password, email, balance)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form  = ChatForm()
    comments = Chat.query.order_by(Chat.message_id.desc())

    name = current_user.username
    message = form.message.data
    timestamp = strftime(" %H:%M - %d %b %Y", gmtime())

    if form.validate_on_submit():
        if request.method == 'GET':
            return render_template('dashboard.html')
        comment = Chat(0, 1, name, message, timestamp)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, name=current_user.username, comments=comments)

@app.route('/logout') #logs out the current user
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
