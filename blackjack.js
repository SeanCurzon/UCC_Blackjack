

	var canvas;
	var context;
	var width;
	var height;
	var interval_id;
	var prev_wallet = 1000;

	var player1 = {
	  card1x:565,
	  card1y:20,
	  card2x:580,
	  card2y:20

	};

	var player2 = {
	  card1x:565,
	  card1y:20,
	  card2x:580,
	  card2y:20

	};

	var player3 = {
	  card1x:565,
	  card1y:20,
	  card2x:580,
	  card2y:20

	};

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
		document.getElementById("myBet").addEventListener("click",betValue);		
		document.getElementById("bet").addEventListener("click",placeBet);
		document.getElementById("newGame").addEventListener("click",newGame);
	}
	function betValue(){

		var slider = document.getElementById("myBet");
		var output = document.getElementById("betValue");

		output.innerHTML = slider.value; // Display the default slider value

		// Update the current slider value (each time you drag the slider handle)
		slider.oninput = function() {
			output.innerHTML = this.value
	
			}

			return(output.innerHTML);
		}
	function placeBet(){
				//allow player to make a bet 

		alert("your bet of "+betValue() +" has been placed");

		var bettop = document.getElementById('betPlaced');
		bettop.innerHTML = "Your Bet: "+betValue();

		var paidtop = document.getElementById('paid');
		paidtop.innerHTML = "Paid: "+(betValue() *2);

		var wallettop = document.getElementById('wallet');

		wallettop.innerHTML = "Wallet: "+(prev_wallet+betValue() *2);
		prev_wallet += (betValue()*2);


		//disable bet button until new game has started
		document.getElementById("bet").disabled=true;

		//get player id and create chip for that player

		var z =4// player id
		var chip = document.createElement("div");
		var bet=  document.createTextNode(betValue());
		chip.id="chip"+z;
		chip.className="chip";
		chip.appendChild(bet);
		document.getElementById("canvas-container").appendChild(chip);
		var chipS = document.createElement("AUDIO");
	  	chipS.src = "graphics/chipsound.mp3"; 
	  	chipS.play()
		

		
		// intialise sound of card being dealt
		var x = document.createElement("AUDIO");
	  	x.src = "graphics/dealCard1.wav";

	    var imageObj = new Image();
 	 	imageObj.onload = function() {
    		deal();
  		};

  function deal() {

    context.drawImage(imageObj, 560, 20, 80, 130); //dealer card

  };

  imageObj.src = 'graphics/cardback.png';



  function movecards(){
  		var pid =1// player id
  		// function to move cards each cad is moved and the image of the card before is cleared
  		// and the image is re drawn with new coordinates
  	
    if (player1.card1y < 440) { //player 1 card 1
		if(player1.card1y == 20){x.play();}
		context.clearRect(0,0,800,750);
		table();
			context.drawImage(imageObj, player1.card1x, player1.card1y, 60, 86);
		    player1.card1x -= 4.75;  
		    player1.card1y += 5;
		
	
	}

    if (player1.card1y >439) {
      if (player2.card1y < 440) { //player 2 card 1
      	if(player2.card1y == 20){x.play();}
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
      		if(player3.card1y == 20){x.play();}

        context.clearRect(0,0,1200,750);
        table();
        context.drawImage(imageObj, player1.card1x, player1.card1y, 80, 129);
        context.drawImage(imageObj, player2.card1x, player2.card1y, 80, 129);
        
        player3.card1x += 1.85;
        player3.card1y += 12;
      }
    }
    if (player3.card1y >439) {
      if (player4.card1y < 440) { //player 4 card 1
      		if(player4.card1y == 20){x.play();}
			

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
        if(player1.card2y == 20){x.play();}

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
      		if(player2.card2y == 20){x.play();}

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

	if(player3.card2y == 0){x.play();}
    if (player2.card2y >439) {
      if (player3.card2y < 440) { //player 3 card 2
      		if(player3.card2y == 20){x.play();}


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
      		if(player4.card2y == 20){x.play();}

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

}

  interval_id=setInterval(movecards, 10);
		}
	

	function table(){

		//function to draw table layout

		var imageObj = new Image();
		imageObj.onload = function() {
			context.drawImage(imageObj,560,0,80,129);
			};
		imageObj.src = 'graphics/cardback.png';
			

		context.strokeStyle = '#A9A9A9';
		context.lineWidth=1;
		context.moveTo(0,400);
		context.lineTo(1200,400);
		context.stroke();

		context.moveTo(0,630);
		context.lineTo(1200,630);
		context.stroke();
//player 1
//206.25
		context.moveTo(150,400);
		context.lineTo(150,630);
		context.stroke();

		context.moveTo(356.25,400);
		context.lineTo(356.25,630);
		context.stroke();

		//betting circle 1

		context.beginPath();
		context.arc(253.125,330,50,0,2*Math.PI);
		context.stroke(); 

//player 2
		context.moveTo(381.25,400);
		context.lineTo(381.25,630);
		context.stroke();

		context.moveTo(587.5,400);
		context.lineTo(587.5,630);
		context.stroke();
	  //betting circle 2
	  
		context.beginPath();
		context.arc(484.375,330,50,0,2*Math.PI);
		context.stroke();

//player 3
		context.moveTo(612.5,400);
		context.lineTo(612.5,630);
		context.stroke();

		context.moveTo(818.75,400);
		context.lineTo(818.75,630);
		context.stroke();

		//betting circle 3
	  
		context.beginPath();
		context.arc(715.625,330,50,0,2*Math.PI);
		context.stroke();

//player 4
		context.moveTo(843.75,400);
		context.lineTo(843.75,630);
		context.stroke();
		
		context.moveTo(1050,400);
		context.lineTo(1050,630);
		context.stroke();
	  //betting circle 4
	  
		context.beginPath();
		context.arc(946.875,330,50,0,2*Math.PI);
		context.stroke();

//DEALER BOX

		
		context.moveTo(600,0);
		context.lineTo(600,750);
	
		context.stroke();

		context.beginPath();
		context.moveTo(445,53);
		context.bezierCurveTo(450,200,750,200,760,53);
		context.strokeStyle = '#000000';
		context.lineWidth = 15;
		context.stroke();

	  }
	
	function newGame(){

		//function to start new game and reset player variable
		clearInterval(interval_id);
		document.getElementById("bet").disabled=false;
		var clearElem = document.getElementById("chip"+1);//player id in here
		clearElem.parentNode.removeChild(clearElem);

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

