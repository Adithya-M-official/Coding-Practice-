from flask import Flask, request, jsonify
from flask_cors import CORS
import Engine

gs = Engine.GameState()
board = gs.board

app = Flask(__name__)
CORS(app)

@app.route("/api/send_state", methods=["GET"])
def send_state():
    return {
        "board" : gs.board.tolist(),
        "whitetomove" : gs.white_to_move,
        "movelog" : gs.move_log,
    };

@app.route("/api/make_move", methods=["POST"])
def post_move():
    global gs, board
    response = request.get()
    data = response.jsonify()
    fromrc, torc, white_moved, from_to_coordinates, piece_type = data['fromrc'], data['torc'], data['whiteMoved'], data["FromToCoordinate"], data['pieceType']

    piece_num = board[fromrc[0]][fromrc[1]]
    board[fromrc[0]][fromrc[1]] = 0
    board[torc[0]][torc[1]] = piece_num

    piece_move = [piece_type, from_to_coordinates]
    gs.white_to_move = not white_moved
    gs.move_log.extend(piece_move)
    
@app.route("/api/make_move", methods=["GET"])
def get_move():
    global board, gs
    return {
        "board" : gs.board.tolist(),
        "whitetomove" : gs.white_to_move,
        "movelog" : gs.move_log,
    };
    

    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    print(gs.board)