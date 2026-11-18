from threading import Thread
from typing import override
from time import sleep


class AiVirtualPlayer(Thread):
    def __init__(self) -> None:
        Thread.__init__(self, name="ai-virtual-player-thread")
        self.__is_running: bool = False

    @override
    def run(self) -> None:
        if not self.__is_running:
            self.__is_running = True
            for counter in range(1_000_000):
                print(f"Valeur du compteur: {counter}")
            self.__is_running = False


class AiReferee(Thread):
    def __init__(self, players_scores: dict[str, int]):
        Thread.__init__(self)
        self.__is_running: bool = False
        assert players_scores is not None
        assert type(players_scores) is dict
        self.__players_scores: dict[str, int] = players_scores

    @override
    def run(self) -> None:
        if not self.__is_running:
            self.__is_running = True
            while self.__is_running:
                print("Scores:")
                for player_score in self.__players_scores.items():
                    print(f"{player_score[0]}: {player_score[1]} points")
                sleep(1)
