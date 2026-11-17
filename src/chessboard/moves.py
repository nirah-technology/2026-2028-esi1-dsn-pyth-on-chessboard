from typing import Protocol, override
from uuid import RESERVED_FUTURE


class MoveStrategy(Protocol):
    def get_targets(self, start_x: int, start_y: int) -> list[tuple[int, int]]: ...


class StraightMove(MoveStrategy):
    def __init__(self, max_steps: int = 8) -> None:
        self.__max_steps = max_steps

    @override
    def get_targets(self, start_x: int, start_y: int) -> list[tuple[int, int]]:
        targets = []

        for step in range(1, self.__max_steps):
            targets.extend(
                [
                    (start_x + step, start_y),
                    (start_x - step, start_y),
                    (start_x, start_y + step),
                    (start_x, start_y - step),
                ]
            )

        return targets


class DigonalMove(MoveStrategy):
    def __init__(self, max_steps: int = 8):
        self.__max_steps = max_steps

    @override
    def get_targets(self, start_x: int, start_y: int) -> list[tuple[int, int]]:
        targets = []

        for step in range(1, self.__max_steps):
            targets.extend(
                [
                    (start_x + step, start_y + step),  # Haut - Droite
                    (start_x - step, start_y + step),  # Haut Gauche
                    (start_x + step, start_y - step),  # Bas Droite
                    (start_x - step, start_y - step),  # Bas Gauche
                ]
            )

        return targets


class KnightMove(MoveStrategy):
    @override
    def get_targets(self, start_x: int, start_y: int) -> list[tuple[int, int]]:
        targets = []

        targets.append((start_x + 1, start_y + 2))
        targets.append((start_x + 1, start_y - 2))
        targets.append((start_x - 1, start_y + 2))
        targets.append((start_x - 1, start_y - 2))

        targets.append((start_x + 2, start_y + 1))
        targets.append((start_x + 2, start_y - 1))
        targets.append((start_x - 2, start_y + 1))
        targets.append((start_x - 2, start_y - 1))

        return targets


class PawnMove(MoveStrategy):
    def __init__(self, direction: int, is_first_move: bool = True) -> None:
        self.__direction: int = direction
        self.__is_first_move: bool = is_first_move

    @override
    def get_targets(self, start_x: int, start_y: int) -> list[tuple[int, int]]:
        targets = []

        targets.append((start_x, start_y + self.__direction))
        if self.__is_first_move:
            targets.append((start_x, start_y + (2 * self.__direction)))

        return targets
