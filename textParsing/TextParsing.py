# coding:utf8

# МОРФОЛОГИЯ
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from nltk import word_tokenize, load_parser, tree
import pymorphy2
from textParsing.syntax2 import MySyntax

morphAnalyzer = pymorphy2.MorphAnalyzer()
# Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
with open('../data/media1.tab', encoding='utf-8') as f:
    sents = list(read_corpus_to_nltk(f))

# Обучаем контекстный теггер на получившемся наборе предложений:
t = PMContextTagger(train=sents, type_="full")

# входной текст
# text = "В нашем классе учатся самые артистичные ученики и ученицы."
text = "В классе учатся ученики"
# разбиваем словосочетание на токены
words1 = word_tokenize(text.lower(), language="russian")

# Применим полученную модель к предложению
tagsDict: list = t.tag(words1)
tagVal: list = [lis[1] for lis in tagsDict]

# for w, tag in t.tag(words1):
#     print(w, morphAnalyzer.lat2cyr(tag))
#     print(w, tag)
# print()
# print()

# вывод только теггов
# list = t.tag(words2)
# for _, tag in list:
#     print(tag)

# СИНТАКСИС
pathToFile = "../resource/book_grammars/test.fcfg"
mySyntax = MySyntax(pathToFile)
mySyntax.pm2fcfg(words1, tagVal, pathToFile, morphAnalyzer)
# построить синтаксический анализатор
cp = load_parser(pathToFile)

# for tree in cp.parse(words1):
#     print(tree)

print()
n = cp.parse(words1)
for obj in n:
    print(obj)
    d = obj.draw()
