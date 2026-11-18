from threading import Lock

from chessboard.ui import WindowGame

from .board import Board, Clock
from .engine import AiReferee, AiVirtualPlayer
from .game import Game
from .human import Human, HumanProxy
from .moves import StraightMove, DigonalMove, KnightMove
from .pieces import PieceBuilder, Piece, Color


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

    players_scores: dict[str, int] = {}
    lock: Lock = Lock()

    ai_player: AiVirtualPlayer = AiVirtualPlayer(
        name="ia", board=board, game=game, players_scores=players_scores, lock=lock
    )
    ai_ref: AiReferee = AiReferee(players_scores=players_scores, lock=lock)

    ai_ref.start()
    ai_player.start()

    # try:
    #     ai_player.join()
    #     ai_ref.join()
    # except:
    #     pass

    ai_player.stop()
    ai_ref.stop()

    game.to_finished_status()

    gui = WindowGame()
    gui.display()
