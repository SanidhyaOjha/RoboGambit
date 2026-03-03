"""
RoboGambit 2025-26 — Task 1: Autonomous Game Engine
Organised by Aries and Robotics Club, IIT Delhi

Board: 6x6 NumPy array
  - 0  : Empty cell
  - 1  : White Pawn
  - 2  : White Knight
  - 3  : White Bishop
  - 4  : White Queen
  - 5  : White King
  - 6  : Black Pawn
  - 7  : Black Knight
  - 8  : Black Bishop
  - 9  : Black Queen
  - 10 : Black King

Board coordinates:
  - Bpttom-left  = A1  (index [0][0])
  - Columns   = A–F (left to right)
  - Rows      = 6-1 (top to bottom)(from white's perspective)

Move output format:  "<piece_id>:<source_cell>-><target_cell>"
  e.g.  "1:B3->B4"   (White Pawn moves from B3 to B4)
"""

import numpy as np
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMPTY = 0

# Piece IDs
WHITE_PAWN   = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 3
WHITE_QUEEN  = 4
WHITE_KING   = 5
BLACK_PAWN   = 6
BLACK_KNIGHT = 7
BLACK_BISHOP = 8
BLACK_QUEEN  = 9
BLACK_KING   = 10

WHITE_PIECES = {WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING}
BLACK_PIECES = {BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING}

BOARD_SIZE = 6

# Column index → letter
COL_TO_FILE = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
FILE_TO_COL = {v: k for k, v in COL_TO_FILE.items()}

# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------

def idx_to_cell(row: int, col: int) -> str:
    """Convert (row, col) zero-indexed to board notation e.g. (0,0) -> 'A1'."""
    return f"{COL_TO_FILE[col]}{row + 1}"

def cell_to_idx(cell: str):
    """Convert board notation e.g. 'A1' -> (row=0, col=0)."""
    col = FILE_TO_COL[cell[0].upper()]
    row = int(cell[1]) - 1
    return row, col

def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def is_white(piece: int) -> bool:
    return piece in WHITE_PIECES

def is_black(piece: int) -> bool:
    return piece in BLACK_PIECES

def same_side(p1: int, p2: int) -> bool:
    return (is_white(p1) and is_white(p2)) or (is_black(p1) and is_black(p2))

# ---------------------------------------------------------------------------
# Move generation  
# ---------------------------------------------------------------------------

def get_pawn_moves(board: np.ndarray, row: int, col: int, piece: int):
    """
    White Pawns move downward (increasing row index).
    Black Pawns move upward  (decreasing row index).
    Captures are diagonal-forward.
    
    """
    
    return moves


def get_knight_moves(board: np.ndarray, row: int, col: int, piece: int):
    moves = []
    
    return moves


def get_sliding_moves(board: np.ndarray, row: int, col: int, piece: int, directions):
    """Generic sliding piece (bishop / queen / rook directions)."""
    moves = []
    
    return moves


def get_bishop_moves(board: np.ndarray, row: int, col: int, piece: int):
    diagonals = [(-1,-1),(-1,1),(1,-1),(1,1)]
    return get_sliding_moves(board, row, col, piece, diagonals)


def get_queen_moves(board: np.ndarray, row: int, col: int, piece: int):
    all_dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    return get_sliding_moves(board, row, col, piece, all_dirs)


def get_king_moves(board: np.ndarray, row: int, col: int, piece: int):
    moves = []
    
    return moves


MOVE_GENERATORS = {
    WHITE_PAWN:   get_pawn_moves,
    WHITE_KNIGHT: get_knight_moves,
    WHITE_BISHOP: get_bishop_moves,
    WHITE_QUEEN:  get_queen_moves,
    WHITE_KING:   get_king_moves,
    BLACK_PAWN:   get_pawn_moves,
    BLACK_KNIGHT: get_knight_moves,
    BLACK_BISHOP: get_bishop_moves,
    BLACK_QUEEN:  get_queen_moves,
    BLACK_KING:   get_king_moves,
}


def get_all_moves(board: np.ndarray, playing_white: bool):
    """Return list of (piece_id, src_row, src_col, dst_row, dst_col) for all legal moves."""
    moves = []
    
    return moves

# ---------------------------------------------------------------------------
# Board evaluation heuristic  (TODO: tune weights / add positional tables)
# ---------------------------------------------------------------------------

PIECE_VALUES = {
    WHITE_PAWN:   100,
    WHITE_KNIGHT: 300,
    WHITE_BISHOP: 320,
    WHITE_QUEEN:  900,
    WHITE_KING:  20000,
    BLACK_PAWN:  -100,
    BLACK_KNIGHT:-300,
    BLACK_BISHOP:-320,
    BLACK_QUEEN: -900,
    BLACK_KING: -20000,
}


def evaluate(board: np.ndarray) -> float:
    """
    Static board evaluation from White's perspective.
    Positive  → advantage for White
    Negative  → advantage for Black
    TODO: Add mobility, piece-square tables, king safety, etc.
    """
    score = 0.0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != EMPTY:
                score += PIECE_VALUES.get(piece, 0)
    return score

# ---------------------------------------------------------------------------
# Search  (Minimax with Alpha-Beta pruning)
# TODO: Add move ordering, quiescence search, iterative deepening, transposition table
# ---------------------------------------------------------------------------

def apply_move(board: np.ndarray, piece, src_row, src_col, dst_row, dst_col) -> np.ndarray:
    new_board = board.copy()
    new_board[src_row][src_col] = EMPTY
    new_board[dst_row][dst_col] = piece
    return new_board


def minimax(board: np.ndarray, depth: int, alpha: float, beta: float,
            maximising: bool) -> float:
    if depth == 0:
        return evaluate(board)

    moves = get_all_moves(board, playing_white=maximising)
    if not moves:
        # No moves available — treat as loss for the side to move
        return -99999 if maximising else 99999

    if maximising:
        best = -float('inf')
        for piece, sr, sc, dr, dc in moves:
            child = apply_move(board, piece, sr, sc, dr, dc)
            val = minimax(child, depth - 1, alpha, beta, False)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break   # Beta cut-off
        return best
    else:
        best = float('inf')
        for piece, sr, sc, dr, dc in moves:
            child = apply_move(board, piece, sr, sc, dr, dc)
            val = minimax(child, depth - 1, alpha, beta, True)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break   # Alpha cut-off
        return best

# ---------------------------------------------------------------------------
# Format move string
# ---------------------------------------------------------------------------

def format_move(piece: int, src_row: int, src_col: int,
                dst_row: int, dst_col: int) -> str:
    """Return move in required format: '<piece_id>:<source_cell>-><target_cell>'."""
    src_cell = idx_to_cell(src_row, src_col)
    dst_cell = idx_to_cell(dst_row, dst_col)
    return f"{piece}:{src_cell}->{dst_cell}"

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def get_best_move(board: np.ndarray, playing_white: bool = True,
                  depth: int = 3) -> Optional[str]:
    """
    Given the current board state, return the best move string.

    Parameters
    ----------
    board        : 6×6 NumPy array representing the current game state.
    playing_white: True if the engine is playing as White, False for Black.
    depth        : Search depth for minimax (increase for stronger play,
                   decrease for faster response).

    Returns
    -------
    Move string in the format '<piece_id>:<src_cell>-><dst_cell>', or
    None if no legal moves are available.
    """
    moves = get_all_moves(board, playing_white)
    if not moves:
        return None

    best_move = None
    best_val  = -float('inf') if playing_white else float('inf')

    for piece, sr, sc, dr, dc in moves:
        child = apply_move(board, piece, sr, sc, dr, dc)
        val   = minimax(child, depth - 1, -float('inf'), float('inf'),
                        not playing_white)

        if playing_white and val > best_val:
            best_val  = val
            best_move = (piece, sr, sc, dr, dc)
        elif not playing_white and val < best_val:
            best_val  = val
            best_move = (piece, sr, sc, dr, dc)

    if best_move is None:
        # Fallback: play first legal move
        best_move = moves[0]

    return format_move(*best_move)


# ---------------------------------------------------------------------------
# Quick smoke-test  
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example: standard-ish starting position on a 6x6 board
    # White pieces on rows 4-5, Black pieces on rows 0-1
    initial_board = np.array([
        [ 7,  8,  9, 10,  8,  7],   # Row 1 (A1–F1) — Black back rank
        [ 6,  6,  6,  6,  6,  6],   # Row 2         — Black pawns
        [ 0,  0,  0,  0,  0,  0],   # Row 3
        [ 0,  0,  0,  0,  0,  0],   # Row 4
        [ 1,  1,  1,  1,  1,  1],   # Row 5         — White pawns
        [ 2,  3,  4,  5,  3,  2],   # Row 6 (A6–F6) — White back rank
    ], dtype=int)

    print("Board:\n", initial_board)
    move = get_best_move(initial_board, playing_white=True, depth=3)
    print("Best move for White:", move)