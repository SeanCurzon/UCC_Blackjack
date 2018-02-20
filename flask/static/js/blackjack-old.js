function rules(){
  alert("*The cards 2 through 10 are worth their face value. \n*Kings, queens, and jacks are each worth 10, and aces may be used as either 1 or 11. \n*The object for the player is to draw cards totaling closer to 21, without going over, than the dealer's cards. \n*The best total of all is a two-card 21, or a blackjack.")
};

var player1 = {
  card1x:365,
  card1y:20,
  card2x:380,
  card2y:20
};

var player2 = {
  card1x:365,
  card1y:20,
  card2x:380,
  card2y:20
};

var player3 = {
  card1x:365,
  card1y:20,
  card2x:380,
  card2y:20
};

var player4 = {
  card1x:365,
  card1y:20,
  card2x:380,
  card2y:20
};

function play(){
  document.getElementById('buttons').innerHTML = "<canvas id='table' width='800' height='700'></canvas>"
  var canvas = document.getElementById('table');
  var context = canvas.getContext('2d');
  var imageObj = new Image();


  imageObj.onload = function() {
    deal();
  };

  function deal() {
    context.drawImage(imageObj, 365, 20, 70, 100); //dealer card
  };

  imageObj.src = 'card.png';

  function movecards(){

    if (player1.card1y < 550) { //player 1 card 1
      context.clearRect(0,0,800,700);
      context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
      player1.card1x -= 9;
      player1.card1y += 15;
    }

    if (player1.card1y >549) {
      if (player2.card1y < 550) { //player 2 card 1
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        player2.card1x -= 3;
        player2.card1y += 15;
      }
    }

    if (player2.card1y >549) {
      if (player3.card1y < 550) { //player 3 card 1
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        player3.card1x += 3;
        player3.card1y += 15;
      }
    }

    if (player3.card1y >549) {
      if (player4.card1y < 550) { //player 4 card 1
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        context.drawImage(imageObj, player4.card1x, player4.card1y, 70, 100);
        player4.card1x += 9;
        player4.card1y += 15;
      }
    }

    if (player4.card1y >549) {
      if (player1.card2y < 550) { //player 1 card 2
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        context.drawImage(imageObj, player4.card1x, player4.card1y, 70, 100);
        context.drawImage(imageObj, player1.card2x, player1.card2y, 70, 100);
        player1.card2x -= 9;
        player1.card2y += 15;
    }
  }

    if (player1.card2y >549) {
      if (player2.card2y < 550) { //player 2 card 2
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        context.drawImage(imageObj, player4.card1x, player4.card1y, 70, 100);
        context.drawImage(imageObj, player1.card2x, player1.card2y, 70, 100);
        context.drawImage(imageObj, player2.card2x, player2.card2y, 70, 100);
        player2.card2x -= 3;
        player2.card2y += 15;
    }
  }

    if (player2.card2y >549) {
      if (player3.card2y < 550) { //player 3 card 2
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        context.drawImage(imageObj, player4.card1x, player4.card1y, 70, 100);
        context.drawImage(imageObj, player1.card2x, player1.card2y, 70, 100);
        context.drawImage(imageObj, player2.card2x, player2.card2y, 70, 100);
        context.drawImage(imageObj, player3.card2x, player3.card2y, 70, 100);
        player3.card2x += 3;
        player3.card2y += 15;
    }
  }

    if (player3.card2y >549) {
      if (player4.card2y < 550) { //player 4 card 2
        context.clearRect(0,0,800,700);
        context.drawImage(imageObj, player1.card1x, player1.card1y, 70, 100);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 70, 100);
        context.drawImage(imageObj, player3.card1x, player3.card1y, 70, 100);
        context.drawImage(imageObj, player4.card1x, player4.card1y, 70, 100);
        context.drawImage(imageObj, player1.card2x, player1.card2y, 70, 100);
        context.drawImage(imageObj, player2.card2x, player2.card2y, 70, 100);
        context.drawImage(imageObj, player3.card2x, player3.card2y, 70, 100);
        context.drawImage(imageObj, player4.card2x, player4.card2y, 70, 100);
        player4.card2x += 10;
        player4.card2y += 19;
    }
  }
}
  setInterval(movecards, 10);
};
