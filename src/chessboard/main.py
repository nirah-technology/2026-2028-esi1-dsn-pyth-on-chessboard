from .board import Board, Clock
from .pieces import PieceBuilder, Piece, Color
from .human import Human, HumanProxy


def main():
    board: Board = Board()
    clock: Clock = Clock()

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
