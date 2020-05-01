# coding:utf8
from pprint import pprint
from nltk import FreqDist
import numpy
import math
from gensim.matutils import jaccard
# spacy
from spacy.tokens import Doc
import spacy_udpipe

# sympy
from sympy import integrate, oo
import sympy.abc as abc

from parsing.approximation_CT import approximation_CT
from parsing.text import Text
from parsing.semantic.Models import Models



trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


class text_metric_analysis:
    """
    Класс вычисления подоббия|метрик документов
    """
    def __init__(self, trainTextUdpipe, text_standart, textsList):
        """

        :param trainTextUdpipe: модель тренировки Udpipe
        :param text_standart: текст эталон (Объект Text)
        :param textsList: список текстов для сравнения (список объектов Text)
        """
        self.trainTextUdpipe = trainTextUdpipe
        # Модель для синтаксичского аналза
        self.nlp = spacy_udpipe.load_from_path(lang="ru",
                                          path=self.trainTextUdpipe,
                                          meta={"description": "Custom 'ru' model"})
        # Инииализация объектов типа Text
        for text in textsList:
            # Получение синтаксической модели
            text.doc = self.nlp(' '.join(text.tokenz))
            # Получение леммы
            text.lemma_text = text.get_lemma_list(text.doc)
            # Получение частоты
            text.freq_dist = self.freq_dist_dic(text.lemma_text)
            # Получение матрицы вероятности
            text.matrix = self.matrix_syntax(text.doc, text.freq_dist)
        # Для текста-эталона
        text_standart.doc = self.nlp(' '.join(text_standart.tokenz))
        text_standart.lemma_text = text_standart.get_lemma_list(text_standart.doc)
        text_standart.freq_dist = self.freq_dist_dic(text_standart.lemma_text)
        text_standart.matrix = self.matrix_syntax(text_standart.doc, text_standart.freq_dist)

    #  Вычисление стахостического подобия текстов
    def stochastic_analysis(self, text_standart: Text, textsList: list):
        """
        вычисление стахостического подобия текстов
        :param text_standart: текст эталон (Объект Text)
        :param textsList: список текстов для сравнения (список объектов Text)
        :return:
        """

        # Инииализация объектов типа Text
        approxim_CT = approximation_CT()
        for text in textsList:
            # Рассчет энтропии
            text.entropy = self.entropy(text.matrix)
            text.entropy2 = self.entropy(text.matrix, entropy2=True)
            text.entropy3 = self.entropy(text.matrix, entropy3=True)
            # Расчет значений аппроксимации
            approxim_CT.get_approximation_value(text)

        text_standart.entropy = self.entropy(text_standart.matrix)
        text_standart.entropy2 = self.entropy(text_standart.matrix, entropy2=True)
        text_standart.entropy3 = self.entropy(text_standart.matrix, entropy3=True)
        approxim_CT.get_approximation_value(text_standart)

        # Вычисление коэфициента подобия(степени схожести)
        self.calculate_p(text_standart, textsList)

        # return text_standart, textsList

    # Вероятность слов в тексте
    def freq_dist_dic(self, lema_list: list):
        """
        Вероятность слов в тексте
        :param lema_list: список лемм текста
        :return: словарь [слово-вероятность]
        """
        # Получение количество встречаемости слова
        freq_dist_pos = FreqDist(lema_list)
        # Получение частоты встречаемости слова(словарь)
        freq_dist_lem = {}
        for k, v in freq_dist_pos.items():
            freq_dist_lem[k] = v / len(freq_dist_pos)
        return freq_dist_lem

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

    # Нахождение стахостического сходства
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

    # Вычисление коэфициента Jaccard
    def distance_metrics_Jaccard(self, text_standart, textsList, models: Models):
        """
        Вычисление метрики Jaccard
        :param text_standart: текст эталон
        :param textsList: список текстов
        :param models: объект типа semantic.Models
        :return:
        """
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(text_standart.lemma_text)
        for text in textsList:
            data_lemmatized_list.append(text.lemma_text)

        # Модель LDA для поиска темы в тексте текста
        model_LDA = models.text_LDA(data_lemmatized_list)

        # Получить мешок слов
        bow_text_standart = model_LDA.id2word.doc2bow(text_standart.lemma_text)
        for text in textsList:
            bow_text = model_LDA.id2word.doc2bow(text.lemma_text)
            # print("jaccard [0 - подобны; 1 - не подобны]")
            # print(jaccard(bow_text_standart, bow_text))
            text.jaccard_coeff = round(jaccard(bow_text_standart, bow_text), 2)

    # Вычисление косинусное сходства документов
    def cosine_similarity(self, text_standart, textsList, models: Models ):
        """
        Вычисление косинусное сходства документов
        :param text_standart: текст эталон
        :param textsList: список текстов
        :param models: объект типа semantic.Models
        :return:
        """
        # Получить список лемм сех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(text_standart.lemma_text)
        for text in textsList:
            data_lemmatized_list.append(text.lemma_text)

        # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
        model_LSI, index = models.text_LSI(data_lemmatized_list)
        vec_text_standart = model_LSI.id2word.doc2bow(text_standart.lemma_text)
        vec_lsi_stand_text = model_LSI[vec_text_standart]  # преобразовать запрос в LSI
        sims = index[vec_lsi_stand_text]  # выполнить запрос сходства с корпусом
        # print("cos [1 - подобны; -1 - не подобны]")
        # print( list(enumerate(sims)))
        list_sims = list(enumerate(sims))
        for i, (n, c) in enumerate(list_sims[1::]):
            textsList[i].cos_sim = round(c, 2)


def main():
    textOriginalList = [textOriginal3, textOriginal2]
    models = Models()
    # Преобразовать в объекты Text
    textsList = []
    for textOriginal in textOriginalList:
        textsList.append(Text(textOriginal))
    text_standart = Text(textOriginal1)

    analysis = text_metric_analysis(trainTextUdpipe, text_standart, textsList)
    analysis.stochastic_analysis(text_standart, textsList)
    analysis.distance_metrics_Jaccard(text_standart, textsList, models)
    analysis.cosine_similarity(text_standart, textsList, models)



if __name__ == '__main__':
    main()
