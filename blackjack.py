from flask import Flask, render_template,request
import random
from dealer import Dealer
from deck import Deck
from card import Card
from player import Player
from hand import Hand


app = Flask(__name__)
"""def main():

    dealer = Dealer()
    player1 = Player(dealer)
    player2 = Player(dealer)
    player3 = Player(dealer)
    player4 = Player(dealer)

    playerlst = [player1,player2,player3,player4]

    for item in playerlst :
        item.startingHand(dealer)

    player4.compareHandAgainstDealer(dealer, player4._mainlst)"""
@app.route('/')
#load gui
def blackjack():
	return render_template('blackjack.html')

@app.route('/betting',methods = ['POST'])
#apply players bet incomplete
def bet():
	return(request.form['myData'])

if __name__ == '__main__':
	main()
