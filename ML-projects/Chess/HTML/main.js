import { GetBoard, initBoard , buildBoard} from "./data.js"
import {GetAndRenderBoard} from "./render.js"

const board = await GetBoard()
async function startApp() {
    const boardData = await initBoard(board)
    GetAndRenderBoard(board, boardData);
}


async function sendMoveToPython(fromrc, torc) {
    const response = await fetch("http://127.0.0.1:5000/api/", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body: JSON.stringify({pieceType: board[fromrc[0]][fromrc[1]]['piece'], from: fromrc, to : torc, whiteMoved: true, FromToCoordinate: [board[fromrc[0]][fromrc[1]]['square'], board[torc[0]][torc[1]]['square']]})
    })

    const data = await response.json()
    const currentBoardData = await buildBoard(data['board'])
    GetAndRenderBoard(data['board'], currentBoardData)
}

function displayClicked() {
    const root = document.getElementById("root")
    root.addEventListener('click',(event)=>{
        const clickedPiece = event.target.closest('.square')
        const showSquare = document.getElementById("moved-piece")
        showSquare.innerHTML = clickedPiece.id
    })
    
}
    
startApp()
displayClicked()