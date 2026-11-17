from typing import Protocol, override

from .constructor_patterns import singleton
from .pieces import Piece


class Observer(Protocol):
    def notify(self, *args, **kwargs): ...


@singleton
class Board:
    # Echequier
    def __init__(self) -> None:
        self.__grid: list[list[Piece]] = [[None] * 8 for _ in range(8)]
        self.__observers: list[Observer] = []

    def subscribe(self, observer: Observer):
        self.__observers.append(observer)

    def move_piece(self, piece_id: int, destination: tuple[int, int]):
        print(
            f"Déplacement de la piece: {piece_id} à l'emplacement X: {destination[0]}, Y: {destination[1]}"
        )

        for observer in self.__observers:
            observer.notify()


@singleton
class Clock(Observer):
    def press(self):
        print("On a appuyé sur le bouton.")

    @override
    def notify(self, *args, **kwargs):
        self.press()
