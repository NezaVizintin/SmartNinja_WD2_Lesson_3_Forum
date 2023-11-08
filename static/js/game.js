/*
var variable = "string"

let mutableVariable = ""

const immutableVariable = ""

// comment

/!*
 more comment
 *!/

let array = [1, 2, 3, "four", ["five"]]

let dictionaryLikeObject = {key1: "value", key2: 2, key3: [1, 2, 3]}

if (mutableVariable == "") {
    console.log("string is empty")
} else {
    console.log("string not empty")
}

let count = 0

while (count < 10) {
    console.log("count is " + count)
    count ++
}

// using let means that the variable number will cease to exist outside the loop, using var would mean the last iteration ob number would remain
for (let number of array) {
    console.log(number)
}

function sum(x, y) {
    return x + y
}

console.log(sum(10,3))
console.log(sum("10",3)) // JS zlima vrednosti skupaj, sešteješ int in string

function deduct(x, y) {
    return x - y
}

console.log(deduct("10",3))  // JS pri odštevanju oba obravnava kot števila - poskuša vedno nekaj izvest, da ne vrže error

console.log("10" == 10) // primerja vrednost ne glede na obliko
console.log("10" === 10) // primerja vrednost IN tip spremenljivke - priporoča se ta enačaj

for (let i = 0; i <= 50; i++) {
    let answer = " "

    if (i % 3 === 0) {
        answer = answer + "Fizz";
    }
    if (i % 5 === 0) {
        answer = answer + "Buzz";
    }
    console.log(i + " " + answer)
}*/


/*var h1Headers = document.getElementsByTagName("h1");

console.log(h1Headers)

setInterval( () => {
    var h1Headers = document.getElementsByTagName("h1");
    h1Headers[0].innerHTML = "." + h1Headers[0].innerHTML;
}, 250)*/
/*

function eventHandler () {
    alert("test");
}

h1Headers.addEventListener("mouseover", eventHandler);*/
/*
const player1 = "x"
const player2 = "o"

var currentPlayer = player1

var board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
    ]

function makeMove(x,y) {
    board[x][y] = "x"

    console.log(board[0])
    console.log(board[1])
    console.log(board[2])
    console.log(".............................")
    switchPlayer()
}

function switchPlayer() {
    if(currentPlayer == player1) {
        currentPlayer = player2
    }
    else {
        currentPlayer = player1
    }
}

function displayBoard() {
    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];

    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];

    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];
    document.getElementsById().innerHTML = board[][];

// OBJECT:

let user = {
    firstName: "Brincelj",
    lastName: "Muc",

    fullName: function() {
        return this.firstName + " " + this.lastName
    }
}
Koristno:

strict mode
caniuse.com

}*/

(function () {

    function displayBoard() {
        document.getElementById('box1-1').innerHTML = board[0][0];
        document.getElementById('box1-2').innerHTML = board[0][1];
        document.getElementById('box1-3').innerHTML = board[0][2];

        document.getElementById('box2-1').innerHTML = board[1][0];
        document.getElementById('box2-2').innerHTML = board[1][1];
        document.getElementById('box2-3').innerHTML = board[1][2];

        document.getElementById('box3-1').innerHTML = board[2][0];
        document.getElementById('box3-2').innerHTML = board[2][1];
        document.getElementById('box3-3').innerHTML = board[2][2];
    }

    const PLAYER_1 = 'X';
    const PLAYER_2 = 'O';

    let currentPlayer = PLAYER_1;

    let board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', ''],
    ];

    document.getElementById("box1-1").addEventListener("click", clickHandler)
    document.getElementById("box1-2").addEventListener("click", clickHandler)
    document.getElementById("box1-3").addEventListener("click", clickHandler)
    document.getElementById("box2-1").addEventListener("click", clickHandler)
    document.getElementById("box2-2").addEventListener("click", clickHandler)
    document.getElementById("box2-3").addEventListener("click", clickHandler)
    document.getElementById("box3-1").addEventListener("click", clickHandler)
    document.getElementById("box3-2").addEventListener("click", clickHandler)
    document.getElementById("box3-3").addEventListener("click", clickHandler)

    function clickHandler(e) {
        id = e.target.id;
        let x = id.substr(-3, 1)
        let y = id.substr(-1, 1)
        makeMove(x, y)
    }

    function makeMove(x, y) {
        if (board[x - 1][y - 1] !== '') {
            alert('Invalid move!!!!')
            return;
        }
        board[x - 1][y - 1] = currentPlayer;

        displayBoard();
        if (isGameFinished()) {
            alert('game finished');
            resetBoard();
        } else {
            switchPlayer();
        }
    }

    function switchPlayer() {
        if (currentPlayer == PLAYER_1) {
            currentPlayer = PLAYER_2;
        } else {
            currentPlayer = PLAYER_1;
        }
    }

    function isGameFinished() {
        // po vrsticah
        if (
            board[0][0] !== '' && board[0][0] == board[0][1] && board[0][0] == board[0][2] ||
            board[1][0] !== '' && board[1][0] == board[1][1] && board[1][0] == board[1][2] ||
            board[2][0] !== '' && board[2][0] == board[2][1] && board[2][0] == board[2][2]
        ) {
            console.log('zmaga po vrsticah');
            return true
        }
        // po stolpcih
        if (
            board[0][0] !== '' && board[0][0] == board[1][0] && board[0][0] == board[2][0] ||
            board[0][1] !== '' && board[0][1] == board[1][1] && board[0][1] == board[2][1] ||
            board[0][2] !== '' && board[0][2] == board[1][2] && board[0][2] == board[2][2]
        ) {
            console.log('zmaga po stolpcih');
            return true
        }
        // po diagonalah
        if (
            board[0][0] !== '' && board[0][0] == board[1][1] && board[0][0] == board[2][2] ||
            board[0][2] !== '' && board[0][2] == board[1][1] && board[0][2] == board[2][0]
        ) {
            console.log('zmaga po diagonali');
            return true;
        }
        return false;
    }
})()


// logika za zmago
// resetiraj igro