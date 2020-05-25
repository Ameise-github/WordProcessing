import typing as t
import pathlib as pl
import itertools as it

from parsing.metric.pragmatic_adequacy import PragmaticAdequacyAlgorithm
from gui.logic.common.pool_tread import BasePoolThread, Combination

PragmaticAdequacyData = t.Tuple[pl.Path, pl.Path]
PragmaticAdequacyIndex = t.Tuple[int, int]


class PragmaticAdequacyThread(BasePoolThread):
    NONE = 0
    FORWARD_ONLY = 1
    REVERSE_ONLY = 2
    BOTH = 3

    def __init__(self,
                 udpipe: t.Optional[pl.Path], text_files: t.List[pl.Path],
                 interlace: t.List[pl.Path], direction: int):
        super().__init__()

        self._udpipe = udpipe
        self._text_files = text_files
        self._interlace = interlace
        self._direction = direction

        self._combinations = []
        self._algorithm = PragmaticAdequacyAlgorithm()

    def prepare(self) -> t.Any:
        forward = self._direction in (self.FORWARD_ONLY, self.BOTH)
        reverse = self._direction in (self.REVERSE_ONLY, self.BOTH)

        indexes = []
        if forward:
            indexes += self._combine_indexes(self._text_files, self._interlace, False)
        if reverse:
            indexes += self._combine_indexes(self._text_files, self._interlace, True)

        self._combinations = self._combine_from_indexes(indexes)

        return indexes

    @staticmethod
    def _combine_indexes(
            sequential: t.List[pl.Path], interlace: t.List[pl.Path],
            reverse: bool) -> t.List[PragmaticAdequacyIndex]:

        # get indexes
        s_indexes = [i for i, _ in enumerate(sequential)]
        i_indexes = [sequential.index(path) for path in interlace]

        # reversed enumerate
        if reverse:
            s_indexes = list(reversed(s_indexes))
            i_indexes = list(reversed(i_indexes))

        # init
        s_len = len(s_indexes)
        result = []

        # calc
        for x, s_index in enumerate(s_indexes):
            if x == s_len - 1:
                break

            next_x = x + 1
            next_index = s_indexes[next_x]

            result.append((s_index, next_index))

            for y, i_index in enumerate(i_indexes):
                if i_index in (s_index, next_index) or i_index not in s_indexes[x::]:
                    continue
                result.append((s_index, i_index))

        # return
        return result

    def _combine_from_indexes(
            self,
            indexes: t.List[PragmaticAdequacyIndex]) -> t.Generator[PragmaticAdequacyData, None, None]:
        for i, j in indexes:
            yield self._text_files[i], self._text_files[j]

    def combine(self) -> t.Generator[Combination, None, None]:
        for comb in self._combinations:
            one, two = comb
            yield Combination(
                comb,
                self._algorithm.process,
                (str(self._udpipe), str(one), str(two))
            )
