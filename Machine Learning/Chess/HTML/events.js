root_div = document.getElementById('root')

function clickedSquare() {
    root_div.addEventListener('click', (event) => {
        clickedSq = event.target.closest(".square")
        return clickedSquare.id
    });
};


export {clickedSquare}