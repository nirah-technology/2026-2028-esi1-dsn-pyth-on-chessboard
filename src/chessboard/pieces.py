from dataclasses import dataclass, field
from enum import Enum


class Color(Enum):
    BLACK = 1
    WHITE = 2


@dataclass(frozen=True)
class Piece:
    id: int
    name: str
    value: int
    color: Color
    moves: list = field(default_factory=list)


class PieceBuilder:
    def __init__(self) -> None:
        self.__id: int = 0
        self.__name: str = None
        self.__value: int = 0
        self.__color: Color = Color.BLACK
        self.__moves: list = list()

    def with_id(self, id: int) -> "PieceBuilder":
        self.__id = id
        return self

    def with_name(self, name: str) -> "PieceBuilder":
        self.__name = name
        return self

    def with_value(self, value: int) -> "PieceBuilder":
        self.__value = value
        return self

    def with_color(self, color: Color) -> "PieceBuilder":
        self.__color = color
        return self

    def with_moves(self, moves: list) -> "PieceBuilder":
        self.__moves.extend(moves)
        return self

    def with_move(self, move: object) -> "PieceBuilder":
        self.__moves.append(move)
        return self

    def build(self) -> Piece:
        return Piece(
            id=self.__id,
            name=self.__name,
            value=self.__value,
            color=self.__color,
            moves=self.__moves,
        )

    @staticmethod
    def create() -> "PieceBuilder":
        return PieceBuilder()
