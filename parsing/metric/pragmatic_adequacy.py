from parsing.metric.base import BaseAlgorithm
from parsing.text import Text


class PragmaticAdequacyAlgorithm(BaseAlgorithm):
    """
    <p><h3>Показатель прагматической адекватности </h3>
    <p>позволяет определить изменения в одном документе</p>
    <p>Если значение показателя <b>равно</b> &laquo;0&raquo;, то добавленные изменения в документ являются <b>бесполезными</b>.<br>
    Если значение показателя <b>больше</b> &laquo;0&raquo;, то добавленные изменения в документ являются <b>полезными</b>.<br>
    Если значение показателя <b>меньше</b> &laquo;0&raquo;, то добавленные изменения в документ являются <b>дезинформацией</b>.</p>
    </p>
    """

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
