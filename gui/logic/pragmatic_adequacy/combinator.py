import typing as t
import pathlib as pl


class PragmaticAdequacyCombinator:
    FORWARD_ONLY = 0
    REVERSE_ONLY = 1
    BOTH = 2

    def __init__(self):
        self.direction = self.FORWARD_ONLY
        self.interlace: t.List[pl.Path] = []
        self.text_files: t.List[pl.Path] = []
        self.udpipe: t.Optional[pl.Path] = None
        self.combination: t.List[t.Tuple[pl.Path, pl.Path]] = []

    @staticmethod
    def _combine(sequential: t.List[pl.Path], interlace: t.List[pl.Path]) -> t.List[t.Tuple[pl.Path, pl.Path]]:
        combination = []
        for s_idx in range(0, len(sequential) - 1):
            c = sequential[s_idx]
            n = sequential[s_idx + 1]
            combination.append((c, n))

            for i_item in interlace:
                if i_item in (c, n) or i_item not in sequential[s_idx::]:
                    continue
                combination.append((c, i_item))

        return combination

    def combine(self) -> None:
        forward = self.direction in (self.FORWARD_ONLY, self.BOTH)
        reverse = self.direction in (self.REVERSE_ONLY, self.BOTH)

        seq = []
        if forward:
            seq += self._combine(self.text_files, self.interlace)
        if reverse:
            seq += self._combine(self.text_files[::-1], self.interlace[::-1])

        self.combination = seq
