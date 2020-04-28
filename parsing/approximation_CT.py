from sympy.abc import t
from sympy import DiracDelta
from parsing.text import Text
import numpy


class approximation_CT:
    def __init__(self):
        self.C1: float = 0
        self.C2: float = 0
        self.T1: float = 0
        self.T2: float = 0

    # формирование первой части функции d
    def return_f(self):
        f = self.C1*DiracDelta(t - self.T1) + self.C2*DiracDelta(t - self.T2)
        return f

    # Получение аппроксимации
    def get_approximation_value(self, text: Text):
        """
        Вычисление значений аппроксимации С и Т
        :param text: объект типа Text
        :return: объект approximation_CT со значеними
        """
        # Расчет значение С1 и С2
        denominator1 = numpy.power(text.entropy3, 2) - 6 * text.entropy3 * text.entropy2 * text.entropy - 3 * \
                       numpy.power(text.entropy2, 2) * numpy.power(text.entropy, 2) + 4 * text.entropy3 * \
                       numpy.power(text.entropy, 3) + 4 * numpy.power(text.entropy2, 3)
        sqrt_d1 = numpy.sqrt(denominator1)
        numerator1 = 3 * text.entropy2 * text.entropy - text.entropy3 - 2 * numpy.power(text.entropy, 3)
        fraction1 = numerator1 / sqrt_d1
        CC1 = 0.5 * (1 + fraction1)
        CC2 = 0.5 * (1 - fraction1)

        # Расчет значений T1 и T2
        denominator2 = 2 * (text.entropy2 - numpy.power(text.entropy, 2))
        TT1 = (text.entropy3 - text.entropy2 * text.entropy - sqrt_d1) / denominator2
        TT2 = (text.entropy3 - text.entropy2 * text.entropy + sqrt_d1) / denominator2

        # Создать значение аппроксимации
        ct_tmp = approximation_CT()
        ct_tmp.C1 = CC1
        ct_tmp.C2 = CC2
        ct_tmp.T1 = TT1
        ct_tmp.T2 = TT2

        return ct_tmp

    def __str__(self) -> str:
        return "CT = [C1 = {}; C2 = {}; T1 = {}; T2 = {}]".format(self.C1, self.C2, self.T1, self.T2)


