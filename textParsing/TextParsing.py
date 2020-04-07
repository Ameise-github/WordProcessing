# coding:utf8

from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from nltk import load_parser, FreqDist, parse
from parsing.syntax.MatrixSyntax import MatrixSyntax
import pymorphy2
from pathlib import Path
import nltk

from parsing.syntax.syntax import MySyntax


textMedia = '../resource/data/media1.tab'
textOriginal = "../resource/data/test1.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/test.fcfg"


def analysText(textMedia, textOriginal, pathToFileGrammer, morphAnalyzer):
    # Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
    with open(textMedia, encoding='utf-8') as f:
        sents = list(read_corpus_to_nltk(f))

    # Обучаем контекстный теггер на получившемся наборе предложений:
    t = PMContextTagger(train=sents, type_="full")

    # Инициализация графематического анализа. Передача в конструктор исходного текста
    graphemAnaliz = GraphematicAnalysis(textOriginal)

    # разбиваем текст на токены
    textTokenz = graphemAnaliz.get_sentences()
    for index, token in enumerate(textTokenz):
        textTokenz[index] = str.lower(token)

    # Применим полученную модель морфологии к предложению
    tagsDict: list = t.tag(textTokenz)

    # СИНТАКСИС
    mySyntax = MySyntax(pathToFileGrammer)
    # Преобразование граматики из вида pymorphy в вид nltk
    mySyntax.pm2fcfg(tagsDict, pathToFileGrammer, morphAnalyzer)
    # Перевести строковое значение в значение URL
    url_path = Path(pathToFileGrammer).absolute().as_uri()
    # построить синтаксический анализатор
    cp = load_parser(url_path, trace=1)
    #Получить синтаксическое дерево
    # trees = cp.chart_parse(textTokenz)
    # for tree in trees:
    #     print(tree)

    #Получение матрицы синтаксического дерева. ПО статье хабра получение матрицы WFST
    grammar = cp.grammar()
    matrixSyntax = MatrixSyntax()
    wfst0 = matrixSyntax.init_wfst(textTokenz, grammar)
    wfst1 = matrixSyntax.complete_wfst(wfst0, textTokenz, grammar)
    # matrixSyntax.display(wfst0, textTokenz)

    return textTokenz, wfst1


morphAnalyzer = pymorphy2.MorphAnalyzer()
tToken, wfst = analysText(textMedia, textOriginal, pathToFileGrammer, morphAnalyzer)
