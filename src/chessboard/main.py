from .game import Game
from .moves import StraightMove, DigonalMove
from src.chessboard.moves import KnightMove

from .board import Board, Clock
from .pieces import PieceBuilder, Piece, Color
from .human import Human, HumanProxy


def main():
    board: Board = Board()
    clock: Clock = Clock()
    board.subscribe(clock)

    builder = PieceBuilder.create()
    white_qween: Piece = (
        builder.with_id(1)
        .with_name("Reine")
        .with_value(9)
        .with_color(Color.WHITE)
        .with_move(StraightMove())
        .with_move(DigonalMove())
        .build()
    )

    builder = PieceBuilder.create()
    black_knight: Piece = (
        builder.with_id(2)
        .with_name("Cavalier Noir")
        .with_value(3)
        .with_color(Color.BLACK)
        .with_move(KnightMove())
        .build()
    )

    kevin: Human = Human()
    kevin.play_turn()
    kevin.think()

    kevin_proxy: HumanProxy = HumanProxy(Human())
    kevin_proxy.play_turn()

    game: Game = Game()
    game.to_playing_status()

    board.move_piece(0, (0, 0))
