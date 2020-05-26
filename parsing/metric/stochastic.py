import math

from parsing.approximation_CT import approximation_CT
from parsing.metric.base import BaseAlgorithm
from parsing.text import Text


class StochasticAlgorithm(BaseAlgorithm):
    """
    <p><h3>Критерий стохастического подобия систем</h3>
    <p>метод сравнивает системы описанные на естественном языке и позволяет перейти к интервальной шкале<br> энтропии с использованием критерия стохастического подобия.</p>
    <p>Если критерий подобия равен <b>&laquo;1&raquo;,</b> значит сравниеваемые системы подобны.<br>
    Если критерий подобия равен <b>&laquo;0&raquo;,</b> значит сравниеваемые системы не подобны.</p>
    </p>
    """

    def __init__(self):
        super().__init__()
        self.name = "Критерий стохастического подобия"

    def process(self, udpipe: str, reference: str, other: str) -> float:
        reference_text = Text(reference, udpipe)
        reference_text.freq_dist_dic()
        reference_text.matrix_syntax()
        reference_text.get_entropy()
        reference_text.CT = approximation_CT(reference_text.entropy, reference_text.entropy2, reference_text.entropy3)

        other_text = Text(other, udpipe)
        other_text.freq_dist_dic()
        other_text.matrix_syntax()
        other_text.get_entropy()
        other_text.CT = approximation_CT(other_text.entropy, other_text.entropy2, other_text.entropy3)

        # Вычисление коэфициента подобия(степени схожести)
        # для отчета
        # f_s = text_standart.CT.return_f()
        # f = get_text.CT.return_f()
        # ff = (f_s - f)**2
        # intgrl = integrate(ff, (abc.t, -oo, oo))
        # # print(intgrl.doit(), intgrl.evalf())
        # if(intgrl != 0 ):
        #     d = math.sqrt(intgrl)
        #     p = 1 - d
        #     print(intgrl, d, p)

        # для рассчета
        ts = reference_text
        t = other_text
        standrt = (ts.CT.C1 * ts.CT.T1) + (ts.CT.C2 * ts.CT.T2)
        tmp = (t.CT.C1 * t.CT.T1) + (t.CT.C2 * t.CT.T2)
        d = math.sqrt(math.pow((standrt - tmp), 2))
        p = 1 - d
        if p < 0:
            t.p = 0.01
        else:
            t.p = round(p, 2)
            # проверка
            # print("tmp = {}; d = {}; p = {}".format(tmp, d, round(p, 2)))

        return other_text.p
