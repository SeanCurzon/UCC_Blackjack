from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_table import Table, Col

app = Flask(__name__)
app.config['SECRET_KEY'] = '314159'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql2223630:aC2%mZ9%@sql2.freemysqlhosting.net/sql2223630'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class GamesTable(db.Model):
    __tablename__="GamesTable"
    gameID=db.Column(db.Integer,db.ForeignKey('ActiveUsers.gameID'),primary_key=True,nullable=False)
    numPlayers=db.Column(db.Integer, index=True, unique=False)
    activeID=db.relationship('ActiveUsers',backref='game',primaryjoin="GamesTable.gameID==ActiveUsers.gameID")
   
class ActiveUsers(db.Model):
    __tablename__="ActiveUsers"
    ID=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30), index=True, unique=True)
    gameID=db.Column(db.Integer,db.ForeignKey('GamesTable.gameID'),nullable=False)
   
class Lobby(Table):
    gameId=Col('ID')
    count=Col('Number of Players')
    users=Col('users')
    

def __init__(self, gameID, numPlayers, username):
    self.gameID = gameID
    self.numPlayers = numPlayers
    self.username = username

#SELECT g.gameID, g.NumPlayers,a.username FROM GamesTable as g, ActiveUsers as a WHERE g.gameID=a.gameID ORDER BY g.gameID desc
games=GamesTable.query.all()
userlist = GamesTable.query.join(ActiveUsers, GamesTable.gameID==ActiveUsers.gameID).add_columns(GamesTable.gameID, GamesTable.numPlayers,ActiveUsers.username).filter(GamesTable.gameID == ActiveUsers.gameID)
#users=ActiveUsers.query.add_columns(ActiveUsers.username).filter(GamesTable.gameID==ActiveUsers.gameID).order_by(GamesTable.gameID.desc()).all()
@app.route('/new_games')    
def new_games():
    return render_template('blackjack.html')
@app.route('/showgame')    
def showgame():
    return render_template('blackjack.html')    
@app.route('/lobby')    
def showgames():
    return render_template('lobby.html',userlist=userlist)
        
if __name__ == '__main__':
    app.run(debug=True)