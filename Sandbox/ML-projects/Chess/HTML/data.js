
const pieceMap = {
    '-1' : "bpawn",
    '-2' : "bknight",
	'-3' : "bbishop",
	'-4': "brook",
	'-5' : "bqueen",
    '-6' : "bking",
    1 : "wpawn",
    2 : "wknight",
    3 : "wbishop",
    4 : "wrook",
    5 : "wqueen",
    6 : "wking",
    0 : null,
};

function Square(color, square, piece, rowcol){
    return {color, square, piece, rowcol};
};


async function GetBoard() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/send_state")
        const data = await response.json()
        return data['board']
    } catch (error) {
        console.log("response", error)
    };
    
};

function SquareRow(rowID, boardData){
    const squareRow = [];
    const abcd = ["a", "b", "c", "d", "e", "f", "g", "h"]
    const assignedrowID = 8-rowID

    boardData[assignedrowID].forEach((square, colidx)=>{
        const coordinate = abcd[colidx]+rowID;
        const isWhite = (assignedrowID+colidx) % 2 === 0;
        const squareColor = isWhite ? "white" : "black";
        const piece = pieceMap[square]
        const rowcol = [assignedrowID, colidx]
        squareRow.push(Square(squareColor, coordinate, piece, rowcol))
    })
    
    return squareRow;
};


async function buildBoard(board) {
    const rows = [];
    for (let index = 8; index > 0; index--) {
        rows.push(SquareRow(index, board));
    };
    return rows;
};

async function initBoard() {
    const board = await GetBoard()
    return buildBoard(board)
};

async function GetPieceData(board, rowcol) {
    return board[rowcol[0]][rowcol[1]]
}


export { GetBoard, initBoard, GetPieceData, buildBoard }