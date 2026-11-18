from threading import Thread, Event, Lock
from typing import override
from time import sleep

from .board import Board
from .game import Game, Status
from .human import AbleToPlayTurnFeature


class AiVirtualPlayer(Thread, AbleToPlayTurnFeature):
    def __init__(
        self,
        name: str,
        board: Board,
        game: Game,
        players_scores: dict[str, int],
        lock: Lock,
    ) -> None:
        Thread.__init__(self, name="ai-virtual-player-thread")
        self.__player_name: str = name
        self.__board: Board = board
        self.__game: Game = game
        self.__players_scores: dict[str, int] = players_scores
        self.__lock: Lock = lock
        self.__stop_event: Event = Event()

    @override
    def play_turn(self):
        with self.__lock:
            if self.__game.status is not Status.PLAYING:
                return
            self.__board.move_piece(2, (2, 3))
            current_score = self.__players_scores.get(self.__player_name, 0)
            self.__players_scores[self.__player_name] = current_score + 1

    @override
    def run(self) -> None:
        moves_played: int = 0
        while not self.__stop_event.is_set():
            self.play_turn()
            moves_played += 1

    def stop(self):
        self.__stop_event.set()


class AiReferee(Thread):
    def __init__(self, players_scores: dict[str, int], lock: Lock):
        Thread.__init__(self)
        assert players_scores is not None

        assert type(players_scores) is dict
        assert isinstance(players_scores, dict)

        self.__players_scores: dict[str, int] = players_scores
        self.__lock: Lock = lock
        self.__stop_event: Event = Event()

    @override
    def run(self) -> None:
        while not self.__stop_event.is_set():
            with self.__lock:
                print("Scores:")
                for player_score in self.__players_scores.items():
                    print(f"{player_score[0]}: {player_score[1]} points")
                self.__stop_event.wait(1.0)

    def stop(self):
        self.__stop_event.set()
