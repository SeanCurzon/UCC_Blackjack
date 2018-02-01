from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

users = open("user.txt", "r")
user = None

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('blackjack.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'pass1' and request.form['username'] == 'player1':
        session['logged_in'] = True
        user = "player1"
    elif request.form['password'] == 'pass2' and request.form['username'] == 'player2':
        session['logged_in'] = True
        user = "player2"
    elif request.form['password'] == 'pass3' and request.form['username'] == 'player3':
        session['logged_in'] = True
        user = "player3"
    elif request.form['password'] == 'pass4' and request.form['username'] == 'player4':
        session['logged_in'] = True
        user = "player4"
    else:
        flash('wrong password!')
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
