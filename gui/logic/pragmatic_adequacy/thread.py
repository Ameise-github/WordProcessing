import typing as t
import pathlib as pl

from parsing.metric.pragmatic_adequacy import PragmaticAdequacyAlgorithm
from gui.logic.common.pool_tread import BasePoolThread


class PragmaticAdequacyData:
    def __init__(self, one: pl.Path = None, two: pl.Path = None):
        self.one = one
        self.two = two

    def __iter__(self):
        return iter((self.one, self.two))


class PragmaticAdequacyThread(BasePoolThread):
    FORWARD_ONLY = 0
    REVERSE_ONLY = 1
    BOTH = 2

    def __init__(self,
                 udpipe: t.Optional[pl.Path], text_files: t.List[pl.Path],
                 interlace: t.List[pl.Path], direction: int):
        super().__init__()

        self._udpipe = udpipe
        self._text_files = text_files
        self._interlace = interlace
        self._direction = direction

    @staticmethod
    def _combine(sequential: t.List[pl.Path], interlace: t.List[pl.Path]) -> t.List[PragmaticAdequacyData]:
        combinations = []
        for s_idx in range(0, len(sequential) - 1):
            current = sequential[s_idx]
            next_ = sequential[s_idx + 1]
            combinations.append(
                PragmaticAdequacyData(current, next_)
            )

            for i_item in interlace:
                if i_item in (current, next_) or i_item not in sequential[s_idx::]:
                    continue
                combinations.append(
                    PragmaticAdequacyData(current, i_item)
                )

        return combinations

    def combine(self) -> list:
        forward = self._direction in (self.FORWARD_ONLY, self.BOTH)
        reverse = self._direction in (self.REVERSE_ONLY, self.BOTH)

        combinations: t.List[PragmaticAdequacyData] = []
        if forward:
            combinations += self._combine(self._text_files, self._interlace)
        if reverse:
            combinations += self._combine(self._text_files[::-1], self._interlace[::-1])

        return combinations

    def prepare_args(self, data: PragmaticAdequacyData):
        algorithm = PragmaticAdequacyAlgorithm()
        return (
            algorithm.process,
            str(self._udpipe),
            str(data.one),
            str(data.two)
        )

    @staticmethod
    def process(args: object) -> object:
        process_func, udpipe, one, two = args
        result = process_func(udpipe, one, two)
        return result
