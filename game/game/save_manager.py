import json
import os

from game.pieces.pawn import Pawn
from game.pieces.rook import Rook
from game.pieces.knight import Knight
from game.pieces.bishop import Bishop
from game.pieces.queen import Queen
from game.pieces.king import King

SAVE_FILE = "saved_game.json"

PIECE_CLASSES = {
    "Pawn": Pawn,
    "Rook": Rook,
    "Knight": Knight,
    "Bishop": Bishop,
    "Queen": Queen,
    "King": King,
}


def save_game(board, current_turn, move_history):
    data = {
        "current_turn": current_turn,
        "move_history": move_history,
        "pieces": []
    }

    for row in range(8):
        for col in range(8):
            piece = board.tiles[row][col].piece

            if piece:
                data["pieces"].append({
                    "type": piece.__class__.__name__,
                    "color": piece.color,
                    "row": piece.row,
                    "col": piece.col
                })

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_game(board):
    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # clear board
    for row in range(8):
        for col in range(8):
            board.tiles[row][col].piece = None

    # recreate pieces
    for p in data["pieces"]:
        piece_class = PIECE_CLASSES[p["type"]]
        piece = piece_class(p["row"], p["col"], p["color"])
        board.tiles[p["row"]][p["col"]].piece = piece

    return data