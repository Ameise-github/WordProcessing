# coding:utf8
from pprint import pprint

import math
from gensim.matutils import jaccard


# sympy
from sympy import integrate, oo
import sympy.abc as abc

from parsing.text import Text
from parsing.semantic.Models import Models


class text_metric_analysis:
    """
    Класс вычисления подобия|метрик документов
    """

    #  Вычисление стахостического подобия текстов
    def stochastic_analysis(self, text_standart: Text, text: Text):
        """
        вычисление стахостического подобия текстов
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Вычисление коэфициента подобия(степени схожести)
        # для отчета
        # f_s = text_standart.CT.return_f()
        # f = text.CT.return_f()
        # ff = (f_s - f)**2
        # intgrl = integrate(ff, (abc.t, -oo, oo))
        # # print(intgrl.doit(), intgrl.evalf())
        # if(intgrl != 0 ):
        #     d = math.sqrt(intgrl)
        #     p = 1 - d
        #     print(intgrl, d, p)

        # для рассчета
        standrt = (text_standart.CT.C1 * text_standart.CT.T1) + (text_standart.CT.C2 * text_standart.CT.T2)
        tmp = (text.CT.C1 * text.CT.T1) + (text.CT.C2 * text.CT.T2)
        d = math.sqrt(math.pow((standrt - tmp), 2))
        p = 1 - d
        if (p < 0):
            text.p = 0.01
        else:
            text.p = round(p, 2)
            # проверка
            # print("tmp = {}; d = {}; p = {}".format(tmp, d, round(p, 2)))

    # Вычисление коэффициента Jaccard
    def distance_metrics_Jaccard(self, text_standart, text):
        """
        Вычисление метрики Jaccard
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(text_standart.lemma_text)
        data_lemmatized_list.append(text.lemma_text)

        # Модель LDA для поиска темы в тексте текста
        models = Models()
        model_LDA = models.text_LDA(data_lemmatized_list)

        # Получить мешок слов
        bow_text_standart = model_LDA.id2word.doc2bow(text_standart.lemma_text)
        bow_text = model_LDA.id2word.doc2bow(text.lemma_text)
        # print("jaccard [0 - подобны; 1 - не подобны]")
        # print(jaccard(bow_text_standart, bow_text))
        text.jaccard_coeff = round(jaccard(bow_text_standart, bow_text), 2)

    # Вычисление косинусное сходства документов
    def cosine_similarity(self, text_standart, text):
        """
        Вычисление косинусное сходства документов
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(text_standart.lemma_text)
        data_lemmatized_list.append(text.lemma_text)

        # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
        models = Models()
        model_LSI, index = models.text_LSI(data_lemmatized_list)
        vec_text_standart = model_LSI.id2word.doc2bow(text_standart.lemma_text)
        vec_lsi_stand_text = model_LSI[vec_text_standart]  # преобразовать запрос в LSI
        sims = index[vec_lsi_stand_text]  # выполнить запрос сходства с корпусом
        # print("cos [1 - подобны; -1 - не подобны]")
        # print( list(enumerate(sims)))
        list_sims = list(enumerate(sims))
        for i, (n, c) in enumerate(list_sims[1::]):
            text.cos_sim = round(c, 2)

    # Вычисление изменений 1-ого документа
    def calculat_I(self, text_old, text_new):
        # разность значений информационной энтропии
        I = text_new.entropy - text_old.entropy

        return round(I, 3)
