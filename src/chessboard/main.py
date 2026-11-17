from .game import Game

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
