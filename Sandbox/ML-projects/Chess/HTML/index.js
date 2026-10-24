import {initBoard} from "./data.js"

const boardData = await initBoard()
for(let index = 0; index < 8; index++) {
    console.log(boardData[index])
}

