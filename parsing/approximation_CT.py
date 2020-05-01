from sympy.abc import t
from sympy import DiracDelta, Heaviside, exp, cos, sin
import numpy


class approximation_CT:
    """
    Класс для получения аппроксимации функции
    """
    def __init__(self):
        self.C1: float = 0
        self.C2: float = 0
        self.T1: float = 0
        self.T2: float = 0
        self.A: float = 0
        self.B: float = 0

    # Получение аппроксимации
    def get_approximation_value(self, text):
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
        CC1 = 1/2 * (1 + fraction1)
        CC2 = 1/2 * (1 - fraction1)

        # Расчет значений T1 и T2
        denominator2 = 2 * (text.entropy2 - numpy.power(text.entropy, 2))
        TT1 = (text.entropy3 - text.entropy2 * text.entropy - sqrt_d1) / denominator2
        TT2 = (text.entropy3 - text.entropy2 * text.entropy + sqrt_d1) / denominator2

        # Создать значение аппроксимации
        text.CT.C1 = CC1
        text.CT.C2 = CC2
        text.CT.T1 = TT1
        text.CT.T2 = TT2

        # return ct_tmp

    # Получение аппроксимации
    def get_approximation_value_hyperexponential(self, text):
        """
        Вычисление значений аппроксимации по гиперэкспоненциальной функции
        :param text: обрабоываемый текст типа Text
        :return:
        """
        AA = text.entropy / (2 * numpy.power(text.entropy, 2) - text.entropy2)
        numeratorB = 3 * numpy.power(text.entropy, 2) - 2 * text.entropy2
        denominatorB = 2 * numpy.power(text.entropy, 2) - text.entropy2
        BB = numpy.sqrt(numpy.sqrt(numeratorB))/denominatorB
        text.CT.A = AA
        text.CT.B = BB

        # return ct_tmp

    # формирование первой части функции d
    def return_f(self):
        """
        Фоомирование функции для интеграла
        :return:
        """
        f = self.C1 * DiracDelta(t - self.T1) + self.C2 * DiracDelta(t - self.T2)
        return f

    # формирование первой части функции d для расчета средней функции
    def return_avg_f(self):
        """
        Формирование фукнцции для интеграла при расчете по формуле
        среднее значение гипердельной и гиперэкспоненциальной функции
        :return:
        """
        denominator1 = (self.C1 * Heaviside(t - self.T1) + self.C2 * Heaviside(t - self.T2)) - 1
        fraction1 = (self.return_f() / denominator1) + \
                    ((self.A * exp(-self.A*t) * sin(self.B * t))/self.B) -\
                    exp(-self.A*t) * cos(self.B * t)
        f = 0.5 * fraction1
        return f

    def __str__(self) -> str:
        return "CT = [C1 = {}; C2 = {}; T1 = {}; T2 = {}; A = {}; B = {}]".format(self.C1, self.C2, self.T1, self.T2, self.A, self.B)
