(function() {

    "use strict";

    // assigns symbol to each player
    const PLAYER_1 = 'X';
    const PLAYER_2 = 'O';

    // sets current player
    let currentPlayer = PLAYER_1;

    //sets empty board
    let board = [
        ['','',''],
        ['','',''],
        ['','',''],
    ];

    // gets board from browser storage and parses it
    let board_saved = JSON.parse(sessionStorage.getItem("board"))

    // if there was a stored board displays that one
    if (board_saved != null) {
        board = board_saved
        displayBoard()
    }

    // registers events - when player clicks on a board space
    document.getElementById('box1-1').addEventListener('click', clickHandler)
    document.getElementById('box1-2').addEventListener('click', clickHandler)
    document.getElementById('box1-3').addEventListener('click', clickHandler)
    document.getElementById('box2-1').addEventListener('click', clickHandler)
    document.getElementById('box2-2').addEventListener('click', clickHandler)
    document.getElementById('box2-3').addEventListener('click', clickHandler)
    document.getElementById('box3-1').addEventListener('click', clickHandler)
    document.getElementById('box3-2').addEventListener('click', clickHandler)
    document.getElementById('box3-3').addEventListener('click', clickHandler)

    // on click handler - extracts coordinates from the element id (string)
    // goes x number of characters back from the end of the string selecting 1 character
    function clickHandler() {
        let x = this.id.substr(-3,1);
        let y = this.id.substr(-1,1);
        makeMove(x, y);
    }

    function makeMove(x, y) {
        // if the player selected field is empty - reponds with alert
        if(board[x-1][y-1] !== '') {
            alert('Invalid move!!!!')
            return;
        }

        // displays the current player symbol on the given coordinates
        board[x-1][y-1] = currentPlayer;

        // displays updated board
        displayBoard();

        // if the game is finished displays message and resets board
        if (isGameFinished()) {
            let a = '123'
            alert('game finished');
            resetBoard();
        }
        // otherwise the player is switched
        else {
            switchPlayer();
        }
    }

    // selects other player
    function switchPlayer() {
        if(currentPlayer == PLAYER_1) {
            currentPlayer = PLAYER_2;
        }else{
            currentPlayer = PLAYER_1;
        }
    }

    // tells the board what to display in each field
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

    // checks if the game is finished
    function isGameFinished() {
        // by row
        if (
            board[0][0] !== '' &&  board[0][0] == board[0][1] && board[0][0] == board[0][2] ||
            board[1][0] !== '' &&  board[1][0] == board[1][1] && board[1][0] == board[1][2] ||
            board[2][0] !== '' &&  board[2][0] == board[2][1] && board[2][0] == board[2][2]
        ) {
            console.log('zmaga po vrsticah');
            return true
        }
        // by column
        if (
            board[0][0] !== '' &&  board[0][0] == board[1][0] && board[0][0] == board[2][0] ||
            board[0][1] !== '' &&  board[0][1] == board[1][1] && board[0][1] == board[2][1] ||
            board[0][2] !== '' &&  board[0][2] == board[1][2] && board[0][2] == board[2][2]
        ) {
            console.log('zmaga po stolpcih');
            return true
        }
        // by diagonal
        if (
            board[0][0] !== '' &&  board[0][0] == board[1][1] && board[0][0] == board[2][2] ||
            board[0][2] !== '' &&  board[0][2] == board[1][1] && board[0][2] == board[2][0]
        ) {
            console.log('zmaga po diagonali');
            return true;
        }
        return false;
    }

    // sets a new board with empty fields
    function resetBoard(){
        board = [
            ['','',''],
            ['','',''],
            ['','',''],
        ];
        currentPlayer = PLAYER_1;
        displayBoard();
    };
}());
