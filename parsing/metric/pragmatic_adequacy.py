from parsing.metric.base import BaseAlgorithm
from parsing.text import Text


class PragmaticAdequacyAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "Показатель прагматической адекватности"

    def process(self, udpipe: str, reference: str, other: str):
        reference_text = Text(reference, udpipe)
        reference_text.freq_dist_dic()
        reference_text.matrix_syntax()
        reference_text.get_entropy()

        other_text = Text(other, udpipe)
        other_text.freq_dist_dic()
        other_text.matrix_syntax()
        other_text.get_entropy()

        # разность значений информационной энтропии
        i_value = other_text.entropy - reference_text.entropy

        return round(i_value, 3)
