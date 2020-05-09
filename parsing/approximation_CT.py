from sympy.abc import t
from sympy import DiracDelta, Heaviside, exp, cos, sin
import numpy


class approximation_CT:
    """
    Класс для получения аппроксимации функции
    """
    def __init__(self, entropy, entropy2, entropy3):
        """

        :param entropy: энтропия 1-ого порядка
        :param entropy2: энтропия 2-ого порядка
        :param entropy3: энтропия 3-ого порядка
        """
        self.C1: float = 0
        self.C2: float = 0
        self.T1: float = 0
        self.T2: float = 0
        self.A: float = 0
        self.B: float = 0
        self.get_approximation_value(entropy, entropy2, entropy3)
        self.get_approximation_value_hyperexponential(entropy, entropy2)


    # Получение аппроксимации
    def get_approximation_value(self, entropy, entropy2, entropy3):
        """
        Вычисление значений аппроксимации С и Т
        :param entropy: энтропия 1-ого порядка
        :param entropy2: энтропия 2-ого порядка
        :param entropy3: энтропия 3-ого порядка
        :return: объект approximation_CT со значеними
        """
        # Расчет значение С1 и С2
        denominator1 = numpy.power(entropy3, 2) - 6 * entropy3 * entropy2 * entropy - 3 * \
                       numpy.power(entropy2, 2) * numpy.power(entropy, 2) + 4 * entropy3 * \
                       numpy.power(entropy, 3) + 4 * numpy.power(entropy2, 3)
        sqrt_d1 = numpy.sqrt(denominator1)
        numerator1 = 3 * entropy2 * entropy - entropy3 - 2 * numpy.power(entropy, 3)
        fraction1 = numerator1 / sqrt_d1
        self.C1 = 1/2 * (1 + fraction1)
        self.C2 = 1/2 * (1 - fraction1)

        # Расчет значений T1 и T2
        denominator2 = 2 * (entropy2 - numpy.power(entropy, 2))
        self.T1 = (entropy3 - entropy2 * entropy - sqrt_d1) / denominator2
        self.T2 = (entropy3 - entropy2 * entropy + sqrt_d1) / denominator2

    # Получение аппроксимации
    def get_approximation_value_hyperexponential(self, entropy, entropy2):
        """
        Вычисление значений аппроксимации по гиперэкспоненциальной функции
        :param entropy: энтропия 1-ого порядка
        :param entropy2: энтропия 2-ого порядка
        :return:
        """
        self.A = entropy / (2 * numpy.power(entropy, 2) - entropy2)
        numeratorB = 3 * numpy.power(entropy, 2) - 2 * entropy2
        denominatorB = 2 * numpy.power(entropy, 2) - entropy2
        self.B = numpy.sqrt(numpy.sqrt(numeratorB))/denominatorB

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
