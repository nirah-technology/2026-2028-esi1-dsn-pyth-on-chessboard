from enum import Enum


class Status(Enum):
    IDLE = 0
    PLAYING = 1
    FINISHED = 2


class Game:
    def __init__(self) -> None:
        self.__status: Status = Status.IDLE

    @property
    def status(self) -> Status:
        return self.__status

    def to_playing_status(self):
        if self.__status is Status.IDLE:
            self.__status = Status.PLAYING
        else:
            raise Exception("Invalid status")

    def to_finished_status(self):
        if self.__status is Status.PLAYING:
            self.__status = Status.FINISHED
        else:
            raise Exception("Invalid status")

    def to_idle_status(self):
        if self.__status is Status.FINISHED:
            self.__status = Status.IDLE
        else:
            raise Exception("Invalid status")
