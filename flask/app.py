from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
import pyodbc
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '314159'
app.config['SQLALCHEMY_DATABASE_URI'] = 'http://sp2018.database.windows.net/'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

server = 'http://sp2018.database.windows.net/' #connecting to DB
database = 'sp2018'
username = 'softwareAdmin'
password = 'software.2018'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

class User(UserMixin, db.Model): #describing DB
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    balance = db.Column(db.String(1000))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm): #define login form for bootstrap
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm): #define registration form for bootstrap
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/') #index page
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) #login page
def login():
    form = LoginForm()

    username = form.username.data
    password = form.username.data

    if form.validate_on_submit(): #when form is validated and subitted
        if cursor.execute("SELECT * FROM Users WHERE user = '%s' AND password = '%s'" % (username,password)): #checks if there is a 'username' with passowrd 'password'
            row = cursor.fetchone()
            login_user(row[1], remember=form.remember.data #logs in the user with username 'row[1]'
            return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    username = form.username.data #collects data from registration form
    password = form.password.data
    email = form.email.data
    balance = 1000

    if form.validate_on_submit():
        cursor.execute("INSERT INTO Users VALUES {%s, %s, %s, %i})" % (username,password,email,balance))
        cnxn.commit() #inserts new user into DB
        return '<h1>New user has been created!</h1>'

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

if __name__ == '__main__':
    app.run(debug=True)
