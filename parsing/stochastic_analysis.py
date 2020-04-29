# coding:utf8
from pprint import pprint
from nltk import FreqDist
import numpy
import math

# spacy
from spacy.tokens import Doc
import spacy_udpipe
from spacy import displacy

# sympy
from sympy import integrate, oo
import sympy.abc as abc

from parsing.approximation_CT import approximation_CT
from parsing.text import Text

trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


class stochastic_analysis:
    """
    Класс вычисления стахостического подоббия документов
    """
    def __init__(self, trainTextUdpipe):
        """

        :param trainTextUdpipe: модель тренировки Udpipe
        """
        self.trainTextUdpipe = trainTextUdpipe
        # Модель для синтаксичского аналза
        self.nlp = spacy_udpipe.load_from_path(lang="ru",
                                          path=self.trainTextUdpipe,
                                          meta={"description": "Custom 'ru' model"})

    def text_analysis(self, textStandart, textOriginalList):
        """
        вычисление стахостического подобия текстов
        :param textStandart: текст эталон
        :param textOriginalList: список текстов для сравнения
        :return: объект Text,  список объектов Text
        """
        # ГРАФЕМАТИКА
        texts = []
        for textOriginal in textOriginalList:
            texts.append(Text(textOriginal))
        text_s = Text(textStandart)

        # Инииализация объектов типа Text
        approxim_CT = approximation_CT()
        for text in texts:
            # Получение синтаксической модели
            text.doc = self.nlp(' '.join(text.tokenz))
            # Получение леммы
            text.lemma_text = self.get_lemma_list(text.doc)
            # Получение частоты
            text.freq_dist = self.freq_dist_dic(text.lemma_text)
            # Получение матрицы вероятности
            text.matrix = self.matrix_syntax(text.doc, text.freq_dist)
            # Рассчет энтропии
            text.entropy = self.entropy(text.matrix)
            text.entropy2 = self.entropy(text.matrix, entropy2=True)
            text.entropy3 = self.entropy(text.matrix, entropy3=True)
            # Расчет значений аппроксимации
            approxim_CT.get_approximation_value(text)

        # Для текста-эталона
        text_s.doc = self.nlp(' '.join(text_s.tokenz))
        text_s.lemma_text = self.get_lemma_list(text_s.doc)
        text_s.freq_dist = self.freq_dist_dic(text_s.lemma_text)
        text_s.matrix = self.matrix_syntax(text_s.doc, text_s.freq_dist)
        text_s.entropy = self.entropy(text_s.matrix)
        text_s.entropy2 = self.entropy(text_s.matrix, entropy2=True)
        text_s.entropy3 = self.entropy(text_s.matrix, entropy3=True)
        approxim_CT.get_approximation_value(text_s)

        # Вычисление коэфициента подобия(степени схожести)
        self.calculate_p(text_s, texts)

        return text_s, texts

    # Вероятность слов в тексте
    def freq_dist_dic(self, lema_list: list):
        """
        Вероятность слов в тексте
        :param lema_list: список лемм текста
        :return: словарь слово-вероятность
        """
        # Получение количество встречаемости слова
        freq_dist_pos = FreqDist(lema_list)
        # Получение частоты встречаемости слова(словарь)
        freq_dist_lem = {}
        for k, v in freq_dist_pos.items():
            freq_dist_lem[k] = v / len(freq_dist_pos)
        return freq_dist_lem

    # Лемматизация слов
    def get_lemma_list(self, doc: Doc):
        """
        Лемматизация слов
        :param doc: полученный документ spacy модели
        :return: список лемм текста
        """
        lema_list = []
        for token in doc:
            lema_list.append(token.lemma_)
        return lema_list

    # Вычисление энтропии
    def entropy(self, matrix_probability, entropy2=False, entropy3=False):
        """
        Вычисление энтропии
        :param matrix_probability: матрица вероятности
        :param entropy2: для рассчета 2-ого начального момента энтропии
        :param entropy3: для рассчета 3-ого начального момента энтропии
        :return: значение энтропии
        """
        s = 0
        for row in matrix_probability:
            for elem in row:
                if (elem != 0):
                    if entropy2:
                        s += numpy.power(elem, 2) * numpy.log2(elem)
                    elif entropy3:
                        s += numpy.power(elem, 3) * numpy.log2(elem)
                    else:
                        s += elem * numpy.log2(elem)
        return -s

    # Получение матрицы
    def matrix_syntax(self, doc, freq_dist_lem: dict):
        """
        Получение вероятностной матрицы
        :param doc: документ полученный из spacy модели
        :freq_dist_lem dict: словарь лемм текста
        :return: матрица ероятности
        """
        n = len(doc)
        matrix = numpy.zeros((n, n), dtype=float)
        for token in doc:
            for child in token.children:
                pi1 = freq_dist_lem[token.lemma_]
                pi2 = freq_dist_lem[child.lemma_]
                matrix[token.i][child.i] = 1 * pi1 * pi2
        return matrix

    # Нахождение сходства
    def calculate_p(self, text_standart: Text, texts: list):
        """
        вычисление степени схожести
        :param text_standart: текст эталон
        :param texts: список текстов
        :return:
        """
        #для отчета
        # f_s = text_standart.CT.return_f()
        # for ts in texts:
        #     f = ts.CT.return_f()
        #     ff = (f_s - f)**2
        #     intgrl = integrate(ff, (abc.t, -oo, oo))
        #     # print(intgrl.doit(), intgrl.evalf())
        #     if(intgrl != 0 ):
        #         d = math.sqrt(intgrl)
        #         p = 1 - d
        #         print(intgrl, d, p)

        #для рассчета
        standrt = (text_standart.CT.C1 * text_standart.CT.T1) + (text_standart.CT.C2 * text_standart.CT.T2)
        for ts in texts:
            tmp = (ts.CT.C1 * ts.CT.T1) + (ts.CT.C2 * ts.CT.T2)
            d = math.sqrt(math.pow((standrt - tmp), 2))
            p = 1 - d
            if( p < 0):
                ts.p = 0.01
            else:
                ts.p = round(p, 2)
            # проверка
            # print("tmp = {}; d = {}; p = {}".format(tmp, d, round(p, 2)))

    # Отображение синтаксического дерева
    def view_syntax_tree(self, pathText):
        """
        Отрисовка синтаксического дерева
        :param pathText: пусть к тексту
        :return:
        """
        text_tmp = Text(pathText)
        text_tmp.doc = self.nlp(' '.join(text_tmp.tokenz))
        html_trees = displacy.render(text_tmp.doc, style="dep")
        return html_trees


def main():
    textOriginalList = [textOriginal3, textOriginal2, textOriginal4]
    analysis = stochastic_analysis(trainTextUdpipe)
    analysis.text_analysis(textOriginal1, textOriginalList)



if __name__ == '__main__':
    main()
