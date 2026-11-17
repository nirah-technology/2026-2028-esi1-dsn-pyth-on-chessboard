from .constructor_patterns import singleton


@singleton
class Board: ...


@singleton
class Clock:
    def press(self): ...
