//fintan
var z =4;
var canvas;
var context;
var width;
var height;
var interval_id;
var dealer;
var prev_wallet;
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

		$.ajax({
		url: "/newhand",
		type: 'GET',
		success: function(response){
			alert(response);
		},
		error: function(error) {
			alert('error');
		}
	});
	//event listeners to react to button presses
	document.getElementById("myBet").addEventListener("click",betValue);		
	document.getElementById("bet").addEventListener("click",placeBet);
	document.getElementById("newGame").addEventListener("click",newHand);
	document.getElementById("hit").addEventListener("click",hit);
	document.getElementById("stand").addEventListener("click",stand);
}
//setInterval(getDB,1000);
//setTimeout(dealersTurn,30000);
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
	// get player id from python script here
	//allow player to make a bet 
	//link betting code form python here

	var myData = betValue();

	$.ajax({
		url: "/bet",
		data: {'bet':myData},
		type: 'POST',
		success: function(response){
			alert("Your Bet: "+myData)
			var wallettop = document.getElementById('wallet');
			wallettop.innerHTML = "Wallet: "+(response);
		},
		error: function(error) {
			alert(error);
		}
	});
	//update the bet field at top of screen
	var bettop = document.getElementById('betPlaced');
	bettop.innerHTML = "Your Bet: "+betValue();
	//disable bet button until new game has started
	document.getElementById("bet").disabled=false;	


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
			choicePhase()
		}
	}
	interval_id=setInterval(movecards, 10);
}	
function choicePhase(){


	var imageObj = new Image();
 	imageObj.onload = function() {
    	deal();
  	};
	function deal() {
	    context.drawImage(imageObj, 560, 0, 80, 129); //dealer card
	   
	};
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
}

function stand(){
	// tell dealer not to give any more cards to the current player
	var noCard = document.createElement('AUDIO');
	//noCard.src = 'static/graphics/sounds/stand.mp3';
	//noCard.play();
		$.ajax({
			url: "/stay",
			type: 'POST',
			data:{'number':z}
				});

		$.ajax({
			url: "/getWinner",
			type: 'POST',
			success: function(response){
				p2 = JSON.parse(response);
				alert(p2);
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
				alert(response)
				var newCard= JSON.parse(response);
				dealNewCard(newCard);
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
				updateInfo(winner);
				}
		});
}
/* function updateInfo(winner){
	if(winner=="You win!"){

		var paidtop = document.getElementById('paid');
		paidtop.innerHTML = "Paid: "+(betValue() *2);
		var wallettop = document.getElementById('wallet');
		wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue()*2);
		prev_wallet += (betValue()*2);
		$.ajax({
			url: "/updatePlayerInfo",
			type: 'POST',
			data: {'paid':true,'amount':prev_wallet}
		});
	}else if (winner == "Draw!"){
		var paidtop = document.getElementById('paid');
		paidtop.innerHTML = "Paid: "+(betValue());
		var wallettop = document.getElementById('wallet');
		wallettop.innerHTML = "Wallet: "+(prev_wallet + betValue());
		prev_wallet += (betValue());

	}else if(winner == "endhand"){
		newHand();
	}else{
		var loser = document.createElement('AUDIO');
		//loser.src = 'static/graphics/sounds/loser.mp3';
		//loser.play();
	}
				if (z==4){
					newGame();
			}
}
*/
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
function continueGame(){	
}
function newHand(){

	$.ajax({
		url: "/newhand",
		type: 'GET',
		success: function(response){
			alert(response);
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
	//table();

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
function newGame(){

	$.ajax({
		url: "/newGame",
		type: 'GET',
		success: function(response){
			alert(response);
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
// everything from this point on is to draw the other players cards and bets and handvalues
function getDB(){
	$.ajax({
		url: "/gameinfo",
		type: 'GET',
		success: function(response){
			if(response['hand1']){
				drawOtherPlayersCards(1,response['hand1'],response['seatnum'])
				drawOtherPlayersCards(2,response['hand2'],response['seatnum'])
			}
			if(response['hand3']){
				drawOtherPlayersCards(3,response['hand3'],response['seatnum'])
			}
			if(response['bet']){
				makeChip(response['seatnum'],response['bet'])
			}
			if (response['stay']){
				showPlayerValue(response['seatnum'],response['handValue'])
			}
			
		},
		error: function(error) {
			console.log(error)	;	}
	});
}

function drawOtherPlayersCards(cardNum,cardName,seatNum){
	var imageObj = new Image();
 	imageObj.onload = function() {
 	
 	// from the ajax request take the players seat number,card name, card number eg is it the first,second or a hit card
 	//draw accordingly

 			//deal out the players first card
 			if (seatNum ==1 && cardNum==1){
 				context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);	
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==2 && cardNum==1){
 				context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==1){
	        	context.drawImage(imageObj, player3.card1x, player3.card1y, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==1){
				context.drawImage(imageObj, player4.card1x, player4.card1y, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}

 			//deal out the players second card
 			else if (seatNum ==1 && cardNum==2){
 				context.drawImage(imageObj, player1.card2x, player1.card2y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";	
 			}
 			else if(seatNum==2 && cardNum==2){
 				context.drawImage(imageObj, player2.card2x, player2.card2y, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==2){
	        	context.drawImage(imageObj, player3.card2x, player3.card2y, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==2){
				context.drawImage(imageObj, player4.card2x, player4.card2y, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}

 			// deal out the hit card
 			else if (seatNum ==1 && cardNum==3){
 				context.drawImage(imageObj, player1.card2x, player1.card2y-15, 80, 129);	
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==2 && cardNum==3){
 				context.drawImage(imageObj, player2.card2x, player2.card2y-15, 80, 129);
 				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==3 &&cardNum==3){
	        	context.drawImage(imageObj, player3.card2x, player3.card2y-15, 80, 129);
	        	imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
 			else if(seatNum==4 && cardNum==3){
				context.drawImage(imageObj, player4.card2x, player4.card2y-15, 80, 129);
				imageObj.src= "static/graphics/deck/"+cardName+".png";
 			}
  	};
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
function showPlayerValue(seatNum,playerValue){
	context.font = "15px Comic Sans MS";
	context.fillStyle = 'white';
	if (seatnum == 1){
		context.fillText('Players Value is: '+playerValue,155,650);
	}
	if (seatnum == 2){
		context.fillText('Players Value is: '+playerValue,385,650);
	}
	if (seatnum == 3){
		context.fillText('Players Value is: '+playerValue,615,650);
	}
	if (seatnum == 4){
		context.fillText('Players Value is: '+playerValue,850,650);
	}
}
console.log("hey");
function dealersTurn(){
	$.ajax({
				url: "/getWinner",
				type: 'GET',
				success: function(response){
					var dealerValue= JSON.parse(response);
					alert('dealers total is:  '+dealerValue);
					endgame();
				}
			});
}