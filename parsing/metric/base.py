import abc


class BaseAlgorithm(abc.ABC):
    def __init__(self):
        self.name = ""

    @abc.abstractmethod
    def process(self, udpipe: str, reference: str, other: str) -> float:
        pass

    def __str__(self) -> str:
        return self.name

