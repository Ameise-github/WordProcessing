# coding:utf8

from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from nltk import load_parser, FreqDist
from nltk.corpus import treebank
import pymorphy2
from pathlib import Path

from parsing.syntax.syntax import MySyntax

morphAnalyzer = pymorphy2.MorphAnalyzer()
textMedia = '../resource/data/media1.tab'
textOriginal = "../resource/data/test1.txt"
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
for index, token in enumerate(textTokenz):
    textTokenz[index] = str.lower(token)

# Применим полученную модель морфологии к предложению
tagsDict: list = t.tag(textTokenz)

# СИНТАКСИС
mySyntax = MySyntax(pathToFileGrammer)
# Преобразование граматики из вида pymorphy в вид nltk
mySyntax.pm2fcfg(tagsDict, pathToFileGrammer, morphAnalyzer)
# построить синтаксический анализатор
# url_path = Path(pathToFileGrammer).absolute().as_uri()
cp = load_parser(pathToFileGrammer, trace=1)
# trees = cp.parse(textTokenz)
# for tree in trees:
#     print(tree)

# print()
#Нарисовать график
# n = cp.parse(textTokenz)
# for obj in n:
#     print(obj)
#     d = obj.draw()
#Подсчет частоты слов
freq = FreqDist(textTokenz)
for key,val in freq.items():
    print (str(key) + ':' + str(val))