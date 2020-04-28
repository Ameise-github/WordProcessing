# coding:utf8
from pprint import pprint
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from nltk import load_parser, FreqDist, parse
import pymorphy2
from pathlib import Path
from parsing.semantic.Models import Models
import numpy
# Gensim
from gensim.matutils import hellinger, jaccard

# spacy
from spacy.tokens import Doc
import spacy_udpipe

from parsing.syntax.MatrixSyntax import MatrixSyntax
from parsing.syntax.syntax import SyntaxAnalysis
from parsing.approximation_CT import approximation_CT
from parsing.text import Text

from sympy.abc import t
from sympy import DiracDelta

trainText = '../resource/data/trainText.tab'
trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/grammarRU.fcfg"


def text_analysis(textStandart, textOriginalList, trainTextUdpipe):
    # ГРАФЕМАТИКА
    texts = []
    for textOriginal in textOriginalList:
        texts.append(Text(textOriginal))
    text_s = Text(textStandart)

    # СИНТАКСИС
    nlp = spacy_udpipe.load_from_path(lang="ru",
                                      path=trainTextUdpipe,
                                      meta={"description": "Custom 'ru' model"})
    for text in texts:
        text.doc = nlp(' '.join(text.tokenz))
    text_s.doc = nlp(' '.join(text_s.tokenz))
    # Инииализация объектов типа Text
    approxim_CT = approximation_CT()
    for text in texts:
        # Получение леммы
        text.lemma_text = get_lemma_list(text.doc)
        # Получение частоты
        text.freq_dist = freq_dist_dic(text.lemma_text)
        # Получение матрицы вероятности
        text.matrix = matrix_syntax(text.doc, text.freq_dist)
        # Рассчет энтропии
        text.entropy = entropy(text.matrix)
        text.entropy2 = entropy(text.matrix, entropy2=True)
        text.entropy3 = entropy(text.matrix, entropy3=True)
        # Расчет значений аппроксимации
        text.CT = approxim_CT.get_approximation_value(text)

    # Для текста-эталона
    text_s.lemma_text = get_lemma_list(text_s.doc)
    text_s.freq_dist = freq_dist_dic(text_s.lemma_text)
    text_s.matrix = matrix_syntax(text_s.doc, text_s.freq_dist)
    text_s.entropy = entropy(text_s.matrix)
    text_s.entropy2 = entropy(text_s.matrix, entropy2=True)
    text_s.entropy3 = entropy(text_s.matrix, entropy3=True)
    text_s.CT = approxim_CT.get_approximation_value(text_s)

    dFxFy(text_s, texts)

    # return


# Вероятность слов в тексте
def freq_dist_dic(lema_list: list):
    """
    Вероятность слов в тексте
    :param lema_list: список лемм текста
    :return: словарь
    """
    # Получение количество встречаемости слова
    freq_dist_pos = FreqDist(lema_list)
    # Получение частоты встречаемости слова(словарь)
    freq_dist_lem = {}
    for k, v in freq_dist_pos.items():
        freq_dist_lem[k] = v / len(freq_dist_pos)
    return freq_dist_lem


# Лемматизация слов
def get_lemma_list(doc: Doc):
    """
    Лемматизация слов
    :param doc: полученный документ spacy модели
    :return:
    """
    lema_list = []
    for token in doc:
        lema_list.append(token.lemma_)
    return lema_list


# Вычисление энтропии
def entropy(matrix_probability, entropy2=False, entropy3=False):
    """
    Вычисление энтропии
    :param matrix_probability: матрица вероятности
    :param entropy2: для рассчета 2-ого начального момента энтропии
    :param entropy3: для рассчета 3-ого начального момента энтропии
    :return:
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
def matrix_syntax(doc, freq_dist_lem: dict):
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


# Нахождение d(Fx,Fy)
def dFxFy(text_standart: Text, texts: list):
    f_s = text_standart.CT.return_f()
    for ts in texts:
        f = ts.CT.return_f()
        ff = f_s - f

    # return d


def main():
    textOriginalList = [textOriginal1, textOriginal2]
    text_analysis(textOriginal1, textOriginalList, trainTextUdpipe)


if __name__ == '__main__':
    main()
