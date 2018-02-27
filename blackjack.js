var canvas;
var context;
var width;
var height;
var interval_id;
var pid;
var dealer;
var dealerStr;
var playerlst = [];
var prev_wallet = 1000;
/* starting coordinates for player 1 cards*/
var player1 = {
	card1x:565,
	card1y:20,
	card2x:580,
	card2y:20
};
/* starting coordinates for player 2 cards*/
var player2 = {
	card1x:565,
	card1y:20,
	card2x:580,
	card2y:20
};
/* starting coordinates for player 3 cards*/
var player3 = {
	card1x:565,
	card1y:20,
	card2x:580,
	card2y:20
};
/* starting coordinates for player 4 cards*/
var player4 = {
	card1x:565,
	card1y:20,
	card2x:580,
	card2y:20
};
document.addEventListener('DOMContentLoaded', init, false);
function init() {  
	canvas = document.querySelector('canvas');
	context = canvas.getContext('2d');
	table();
	//event listeners to react to button presses
	document.getElementById("myBet").addEventListener("click",betValue);		
	document.getElementById("bet").addEventListener("click",placeBet);
	document.getElementById("newGame").addEventListener("click",newGame);
}
function betValue(){

	var slider = document.getElementById("myBet");
	var output = document.getElementById("betValue");
	// Display the default slider value
	output.innerHTML = slider.value; 
	// Update the current slider value (each time you drag the slider handle)
	slider.oninput = function() {
		output.innerHTML = this.value
	}
	return(output.innerHTML);
}
function placeBet(){
	var z =4// get player id from python script here
	//allow player to make a bet 
	//link betting code form python here

	var myData = betValue();

	$.ajax({
		url: "/betting",
		data: { "myData" : myData , "player" : z},
		type: 'POST',
		success: function(response){
			alert(response);
		},
		error: function(error) {
			alert(error);
		}
	});
	//update the bet field at top of screen
	var bettop = document.getElementById('betPlaced');
	bettop.innerHTML = "Your Bet: "+betValue();
	// update wallet field at top of the screen
	var wallettop = document.getElementById('wallet');
	wallettop.innerHTML = "Wallet: "+(prev_wallet - betValue());
	prev_wallet -= (betValue());
	//disable bet button until new game has started
	document.getElementById("bet").disabled=true;	



	//get player id and create chip for that player
	//get list of other players bets	
	for(z=1;z<4;z++){
		makeChip(z,10)//put player id andthere bet value as variable here values taken from ajax get
	}

	// will become redundant once code is fully linked with server and database
	var chip = document.createElement("div");
	var bet=  document.createTextNode(betValue());
	chip.id="chip"+4;//4 will be replaced by player id
	chip.className="chip";
	chip.appendChild(bet);
	document.getElementById("canvas-container").appendChild(chip);
	var chipS = document.createElement("AUDIO");
	//chipS.src = "static/graphics/sounds/chipsound.mp3"; 
	//chipS.play()	


	// intialise sound of card being dealt
	var x = document.createElement("AUDIO");
	//x.src = "static/graphics/sounds/dealcard1.wav";
	//intailise image object
	var imageObj = new Image();
 	imageObj.onload = function() {};

	//console.log(dealerCard['responseText'][1]);
	function movecards(){
	  	// function to move cards each cad is moved canvas cleared
	  	// and the image is re drawn with new coordinates
	  	// add line to each if statement that takes the card value from python code
  	  	// and draws according image
	  imageObj.src = "static/graphics/cardback.png";
	   if (player1.card1y < 440) { //player 1 card 1
			if(player1.card1y == 20){
				//x.play();
			}
				context.clearRect(0,0,1200,750);
				table();
				context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
			    player1.card1x -= 4.75;  
			    player1.card1y += 5;
			}
		
	    if (player1.card1y >439) {
	      	if (player2.card1y < 440) { //player 2 card 1
		      	if(player2.card1y == 20){
		      		//x.play();
		      	}
		      	context.clearRect(0,0,1200,750);
		        table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        player2.card1x -= 3.75;
	        	player2.card1y += 10;    
	      	}
	    }

	    if (player2.card1y >439) {
	      	if (player3.card1y < 440) { //player 3 card 1
	      		if(player3.card1y == 20){
	      			//x.play();
	      		}
		        context.clearRect(0,0,1200,750);
		        table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y,80, 129);
		        player3.card1x += 1.85;
		        player3.card1y += 12;
	      	}
	    }

	    if (player3.card1y >439) {
	      	if (player4.card1y < 440) { //player 4 card 1
	      		if(player4.card1y == 20){
	      			//x.play();
	      		}
		      	context.clearRect(0,0,1200,750);
		      	table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y,80, 129);
		        context.drawImage(imageObj, player4.card1x, player4.card1y,80, 129);
		        player4.card1x += 10.5;
		        player4.card1y += 15;
	      	}
	    }

	    if (player4.card1y >439) {
	      	if (player1.card2y < 440) { //player 1 card 2
		        if(player1.card2y == 20){
		        	//x.play();
		        }
				context.clearRect(0,0,1200,750);
		        table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
		        context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
		        context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
		        player1.card2x -= 14.35;
		        player1.card2y += 15;
	    	}
	  	}

	    if (player1.card2y >439) {
	      	if (player2.card2y < 440) { //player 2 card 2
	      		if(player2.card2y == 20){
	      			//x.play();
	      		}
		        context.clearRect(0,0,1200,750);
		        table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
		        context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
		        context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
		        context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
		        player2.card2x -= 5.75;
		        player2.card2y += 15;
	    	}
	  	}

	    if (player2.card2y >439) {
	      	if (player3.card2y < 440) { //player 3 card 2
	      		if(player3.card2y == 20){
	      			//x.play();
	      		}
		        context.clearRect(0,0,1200,750);
		        table();
		     	context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
		        context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
		        context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
		        context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
		        context.drawImage(imageObj, player3.card2x, player3.card2y, 80, 129);
		        player3.card2x += 2.15;
		        player3.card2y += 15;
	    	}
	  	}

	    if (player3.card2y >439) {
	      	if (player4.card2y < 450) { //player 4 card 2
	      		if(player4.card2y == 20){//play dealing sound
	      			//x.play();
	      		}
		        context.clearRect(0,0,1200,750);
		        table();
		        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		        context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
		        context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
		        context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
		        context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
		        context.drawImage(imageObj, player3.card2x, player3.card2y, 80, 129);
		        context.drawImage(imageObj, player4.card2x, player4.card2y, 80, 129);
		        player4.card2x += 10.45;
		        player4.card2y += 15;
	    	}
	  	}

		// check if final card has been dealt to player 4
		if(player4.card2y == 455){
			/*imageObj.src= "static/graphics/deck/3ofHearts.png";
		    context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
		    imageObj.src= "static/graphics/deck/3ofHearts.png";
		    context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
		    imageObj.src= "static/graphics/deck/3ofHearts.png";
	        context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
	        imageObj.src= "static/graphics/deck/3ofHearts.png";
	        context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
	        imageObj.src= "static/graphics/deck/3ofHearts.png";	        
	        context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
	        imageObj.src= "static/graphics/deck/8ofHearts.png";
	        context.drawImage(imageObj, player3.card2x, player3.card2y, 80, 129);
	       /*	imageObj.src= "static/graphics/deck/3ofClubs.png";
	        context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
	        imageObj.src= "static/graphics/deck/3ofClubs.png";
	        context.drawImage(imageObj, player4.card2x-10.45, player4.card2y=15, 80, 129);*/
			choicePhase()
		}
	}
	interval_id=setInterval(movecards, 10);

}	

function makeChip(playerId,betVal){
	var chip = document.createElement("div");
	var bet=  document.createTextNode(betVal);
	chip.id="chip"+playerId;
	chip.className="chip";
	chip.appendChild(bet);
	document.getElementById("canvas-container").appendChild(chip);
	var chipS = document.createElement("AUDIO");
	//chipS.src = "static/graphics/sounds/chipsound.mp3"; 
	//chipS.play()
}
function choicePhase(){


	var imageObj = new Image();
 	imageObj.onload = function() {
    	deal();
  	};
	function deal() {
	    context.drawImage(imageObj, 560, 0, 80, 129); //dealer card
	   
	};
	console.log('here');
	$.ajax({
			url: "/cardValue",
			type: 'GET',
			
			success: function(response){
				
				dealer = JSON.parse(response);
				alert('dealers first card is: '+dealer);
				imageObj.src = "static/graphics/deck/"+dealer+".png";
				//return dealer
			}
		});

var imageObj2 = new Image();
 	imageObj2.onload = function() {
    	deal2();
  	};
	function deal2() {
		context.drawImage(imageObj2, player4.card1x, player4.card1y, 80, 129);
	};

	$.ajax({
			url: "/playerCardValue1",
			type: 'GET',
			success: function(response){
				
				p1 = JSON.parse(response);
				alert("players first card is: "+p1);
				console.log(p1);
				imageObj2.src = "static/graphics/deck/"+p1+".png";
				//return dealer
			}
		});
	var imageObj3 = new Image();
 	imageObj3.onload = function() {
    	deal3();
  	};
	function deal3() {
		    context.drawImage(imageObj3, player4.card2x-10.45, player4.card2y-15, 80, 129);
	};
	$.ajax({
			url: "/playerCardValue2",
			type: 'GET',
			success: function(response){
				p2 = JSON.parse(response);
				alert('players Second card is: '+p2);
				console.log(p2);
				imageObj3.src = "static/graphics/deck/"+p2+".png";
				//return dealer
			}
		});

	// called once all cards are dealt
	// cycle through players if any balck jacks update wallet accordingly set winner to true
	// ask players to make a choice playerChoices() if stand move on to next player
	// if hit and player goes bust set winner to false
	// else ask again until player busts or stands
	// run compare hand from python =code and update each players wallet accordingly
	clearInterval(interval_id);
	playerChoices()
}
function getHand(cardValue){
	if(cardValue[1] == "A"){
		var cardValue = 11;
	}
	else if(cardValue[1] == "K"){
		var cardValue = 10;
	}
	else if(cardValue[1] == "J"){
	    var cardValue = 10;
    }
    else if(cardValue[1] == "Q"){		 
        var cardValue = 10;
   }
    else if(cardValue[1] == "1"){
	    var cardValue = 10;
	}else{
		var cardValue = parseInt(cardValue[1]);
	}

	console.log(cardValue)
	$.ajax({
			url: "/handValue",
			data: { "cardValue" : cardValue},
			type: 'POST',
			success: function(response){
				var handValue= JSON.parse(response);
				alert('players hand is:  '+handValue);
				if (handValue>21){ 
				 	endgame();
				}
			}
		});
}
function playerChoices(){

	// put in function to cycle through players nby getting player list starting at player 1
	//and end at player4
	//alert(hit);
	//let player choose hit or stand
	document.getElementById("hit").addEventListener("click",hit);
	document.getElementById("stand").addEventListener("click",stand);

}
function stand(){
	// tell dealer not to give any more cards to the current player
	var noCard = document.createElement('AUDIO');
	//noCard.src = 'static/graphics/sounds/stand.mp3';
	//noCard.play();

	//get dealers total
	$.ajax({
			url: "/dealerValue",
			type: 'GET',
			success: function(response){
				var dealerValue= JSON.parse(response);
				alert('dealers total is:  '+dealerValue);
				endgame();
			}
		});


}
function hit(){
	//add code to get value of card from python code and calculate new value
	// if bust play losing sounds
	// else move on or hit
	$.ajax({
			url: "/hit",
			type: 'GET',
			success: function(response){
				var newCard= JSON.parse(response);
				alert(newCard);
				dealNewCard(newCard);
		       getHand(response);
			}
		});
}
function dealNewCard(source){

	var imageObj4 = new Image();
 	imageObj4.onload = function() {
    	deal4();
  	};
	function deal4() {
      context.drawImage(imageObj4, player4.card2x, player4.card2y-15, 80, 129);
	};

	imageObj4.src = "static/graphics/deck/"+source+".png";
}

function endgame(){

	$.ajax({
			url: "/getWinner",
			type: 'GET',
			success: function(response){
				var winner= response;
				alert(winner);


				if(winner[0]=="p"){
					var paidtop = document.getElementById('paid');
					paidtop.innerHTML = "Paid: "+(betValue() *2);
					var wallettop = document.getElementById('wallet');
					wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue()*2);
					prev_wallet += (betValue()*2);
				}else if (winner[1] == "r"){
					var paidtop = document.getElementById('paid');
					paidtop.innerHTML = "Paid: "+(betValue());
					var wallettop = document.getElementById('wallet');
					wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue());
					prev_wallet += (betValue());

				}else{
					var loser = document.createElement('AUDIO');
					//loser.src = 'static/graphics/sounds/loser.mp3';
					//loser.play();
				}
				newGame();
			}
		});
}
function table(){

	//function to draw table layout
	//var imageObj = new Image();
	//imageObj.onload = function() {
	//	context.drawImage(imageObj,560,0,80,129);
	//};
		
	//imageObj.src = "static/graphics/cardback.png" ;
	//top line of player field			
	context.strokeStyle = '#A9A9A9';
	context.lineWidth=2;
	context.moveTo(0,400);
	context.lineTo(1200,400);
	//bottomline of player fields
	context.moveTo(0,630);
	context.lineTo(1200,630);
	//player 1 left border
	context.moveTo(150,400);
	context.lineTo(150,630);
	//player 1 right border
	context.moveTo(356.25,400);
	context.lineTo(356.25,630);
	//player 2 left border
	context.moveTo(381.25,400);
	context.lineTo(381.25,630);
	//right border
	context.moveTo(587.5,400);
	context.lineTo(587.5,630);
	//player 3 left border
	context.moveTo(612.5,400);
	context.lineTo(612.5,630);
	//right border
	context.moveTo(818.75,400);
	context.lineTo(818.75,630);
	//player 4 left border
	context.moveTo(843.75,400);
	context.lineTo(843.75,630);
	//right border
	context.moveTo(1050,400);
	context.lineTo(1050,630);
	context.stroke();
	//betting circle 1
	context.beginPath();
	context.arc(253.125,330,50,0,2*Math.PI);
	context.stroke();
	//betting circle 2
	context.beginPath();
	context.arc(484.375,330,50,0,2*Math.PI);
	context.stroke();
	//betting circle 3
	context.beginPath();
	context.arc(715.625,330,50,0,2*Math.PI);
	context.stroke();
	//betting circle 4 
	context.beginPath();
	context.arc(946.875,330,50,0,2*Math.PI);
	context.stroke();
	//DEALER BOX
	context.beginPath();
	context.moveTo(445,53);
	context.bezierCurveTo(450,200,750,200,760,53);
	context.strokeStyle = '#000000';
	context.lineWidth = 15;
	context.stroke();
}
function newGame(){

	$.ajax({
		url: "/newGame",
		type: 'GET',
		success: function(response){
			alert(response);
			playerlst = response
		},
		error: function(error) {
			alert('error');
		}
	});
	//function to start new game and reset player variableS
	document.getElementById("bet").disabled=false;
	for(z=1;z<5;z++){
		var clearElem = document.getElementById("chip"+z);//player id in here
		clearElem.parentNode.removeChild(clearElem);
	}
	context.clearRect(0,0,1200,750);
	table();

	player1 = {
		card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player2 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player3 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};

	player4 = {
	  	card1x:565,
	  	card1y:20,
	  	card2x:580,
	  	card2y:20
	};	
}
