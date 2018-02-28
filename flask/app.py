#!/bin/env python
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/mysql'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='mysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor(pymysql.cursors.DictCursor)

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
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout') #logs out the current user
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
        emit('my response',
             {'message': '{0} has joined'.format(current_user.name)},
             broadcast=True)
    else:
        return False  # not allowed here

if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True)
