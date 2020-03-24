# coding:utf8

from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from nltk import load_parser
from nltk.corpus import treebank
import pymorphy2

from parsing.syntax.syntax import MySyntax

morphAnalyzer = pymorphy2.MorphAnalyzer()
textMedia = '../resource/data/media1.tab'
textOriginal = "../resource/data/text2.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/test.fcfg"

# Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
with open(textMedia, encoding='utf-8') as f:
    sents = list(read_corpus_to_nltk(f))

# Обучаем контекстный теггер на получившемся наборе предложений:
t = PMContextTagger(train=sents, type_="full")

# Инициализация графематического анализа. Передача в конструктор исходного текста
graphemAnaliz = GraphematicAnalysis(textOriginal)

# разбиваем текст на токены
textTokenz = graphemAnaliz.get_sentences()

# Применим полученную модель морфологии к предложению
tagsDict: list = t.tag(textTokenz)
tagVal: list = [lis[1] for lis in tagsDict]

# СИНТАКСИС
mySyntax = MySyntax(pathToFileGrammer)
# Преобразование граматики из вида pymorphy в вид nltk
mySyntax.pm2fcfg(textTokenz, tagVal, pathToFileGrammer, morphAnalyzer)
# построить синтаксический анализатор
cp = load_parser(pathToFileGrammer)

# for tree in cp.parse(words1):
#     print(tree)
t = treebank.parsed_sents('wsj_0001.mrg')[1]
t.draw()

# print()
# n = cp.parse(words1)
# for obj in n:
#     print(obj)
#     d = obj.draw()
