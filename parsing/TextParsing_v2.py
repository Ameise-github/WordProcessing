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

trainText = '../resource/data/trainText.tab'
trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/grammarRU.fcfg"


def text_analysis(textOriginalList, trainTextUdpipe):
    # ГРАФЕМАТИКА
    # Инициализация графематического анализа. Передача в конструктор исходного текста
    graphemAnalizList = []
    for textOriginal in textOriginalList:
        graphemAnalizList.append(GraphematicAnalysis(textOriginal))

    # разбиваем текст на токены
    textTokenzList = []
    for graphemAnaliz in graphemAnalizList:
        textTokenzList.append(graphemAnaliz.get_sentences())

    # СИНТАКСИС
    nlp = spacy_udpipe.load_from_path(lang="ru",
                                      path=trainTextUdpipe,
                                      meta={"description": "Custom 'ru' model"})
    docs = []
    for textT in textTokenzList:
        docs.append(nlp(' '.join(textT)))

    # Получение матрицы вероятности
    matrices = matrix_syntax(docs)
    # Рассчет энтропии
    entropy_list = []
    entropy_list2 = []
    entropy_list3 = []
    for matrix in matrices:
        entropy_list.append(entropy(matrix))
        entropy_list2.append(entropy(matrix, entropy2=True))
        entropy_list3.append(entropy(matrix, entropy3=True))


    # return


# Частота слов в тексте
def freq_dist_dic(doc: Doc):
    # Поулчение лемм
    lema_list = get_lemma_list(doc)
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
    :param tokenPosList: Лист токенов
    :return:
    """
    lema_list = []
    for token in doc:
        lema_list.append(token.lemma_)
    return lema_list


# Вычисление энтропии
def entropy(matrix_probability, entropy2 = False, entropy3 = False):
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
def matrix_syntax(docs):
    matrixs = []
    for i, doc in enumerate(docs):
        n = len(doc)
        matrix = numpy.zeros((n, n), dtype=float)
        freq_dist_lem = freq_dist_dic(doc)
        for token in doc:
            for child in token.children:
                pi1 = freq_dist_lem[token.lemma_]
                pi2 = freq_dist_lem[child.lemma_]
                matrix[token.i][child.i] = 1 * pi1 * pi2
        matrixs.append(matrix)
    return matrixs


def main():
    textOriginalList = [textOriginal1, textOriginal2]
    text_analysis(textOriginalList, trainTextUdpipe)


if __name__ == '__main__':
    main()
