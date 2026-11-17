from typing import Protocol


class AbleToPlayTurnFeature(Protocol):
    def play_turn(self): ...


class Human(AbleToPlayTurnFeature):
    def play_turn(self):
        print("J'ai joué mon tour.")

    def think(self):
        print("Je réffléchie...")


class HumanProxy(AbleToPlayTurnFeature):
    def __init__(self, human: Human) -> None:
        self.__human: Human = human

    def play_turn(self):
        print("C'est à moi de jouer !!")
        self.__human.play_turn()
        print("C'est, j'ai fini de jouer.")
