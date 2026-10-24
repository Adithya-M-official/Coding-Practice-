
const root_div= document.getElementById("root") 

const imgMap = {
    '-1' : "../Pieces/b_pawn_svg_NoShadow.svg",
    '-2' : "../Pieces/b_knight_svg_NoShadow.svg",
	'-3' : "../Pieces/b_bishop_svg_NoShadow.svg",
	'-4': "../Pieces/b_rook_svg_NoShadow.svg",
	'-5' : "../Pieces/b_queen_svg_NoShadow.svg",
    '-6' : "../Pieces/b_king_svg_NoShadow.svg",
    1 : "../Pieces/w_pawn_svg_NoShadow.svg",
    2 : "../Pieces/w_knight_svg_NoShadow.svg",
    3 : "../Pieces/w_bishop_svg_NoShadow.svg",
    4 : "../Pieces/w_rook_svg_NoShadow.svg",
    5 : "../Pieces/w_queen_svg_NoShadow.svg",
    6 : "../Pieces/w_king_svg_NoShadow.svg",
    0 : " "
};

const colchars = ['a','b','c','d','e','f','g','h']
async function GetAndRenderBoard(board,boardData){
    try {
        board.forEach((row, rowidx) => {
            const rowel= document.createElement("div")
            rowel.classList.add("squareRow")
            
            row.forEach((square, colidx) => {
                const squareEl = document.createElement("div")

                const isWhiteSquare = (rowidx + colidx) %2 === 0;
                const squarecolor = isWhiteSquare ? "white" : "black";

                const squareCoordinate = boardData[rowidx][colidx]['square']
                
                squareEl.classList.add(squarecolor, "square")
                squareEl.id = squareCoordinate
                
                if(colidx===0){
                    const numEl = document.createElement('p')
                    numEl.textContent = `${8-rowidx}`
                    numEl.id = 'row-num'
                    const numColor = isWhiteSquare ? 'black' : 'white';
                    
                    numEl.classList.add(numColor)
                    squareEl.appendChild(numEl)
                }

                if(rowidx === 7){
                    const charEl = document.createElement('p')
                    charEl.textContent = colchars[colidx]
                    charEl.id = 'col-char'
                    const charColor = isWhiteSquare ? 'black' : 'white';
                    charEl.classList.add(charColor)
                    squareEl.appendChild(charEl)
                }
                
                
                if (square !== 0 && imgMap[square]) {
                    const img = document.createElement("img")
                    img.src = imgMap[square]
                    img.style.height = "75%";
                    img.style.width = "75%";
                    squareEl.appendChild(img)
                };

                
                rowel.appendChild(squareEl)
            });
            root_div.appendChild(rowel)
        });
    } catch(error) {
        console.log("RenderingIssue", error)
    };
};




export {GetAndRenderBoard};