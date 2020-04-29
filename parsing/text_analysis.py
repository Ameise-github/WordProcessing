# coding:utf8
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
import pymorphy2


def morph_analysis(trainTextNLTK4russian, textOriginal):
    # Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
    with open(trainTextNLTK4russian, encoding='utf-8') as f:
        sents = list(read_corpus_to_nltk(f))

    # Обучаем контекстный теггер на получившемся наборе предложений:
    contextTegger = PMContextTagger(train=sents, type_="full")

    # Инициализация графематического анализа. Передача в конструктор исходного текста
    graphemAnaliz = GraphematicAnalysis(textOriginal)

    # разбиваем текст на токены
    textTokenz = graphemAnaliz.get_sentences()

    # Применим полученную модель морфологии к тексту
    tagsDict = contextTegger.tag(textTokenz)

    tokenPosList = get_tag_pymorphy(tagsDict)

    return tokenPosList


# Получить tag как объект pymorphy2
def get_tag_pymorphy(tagsDict):
    morphAnalyz = pymorphy2.MorphAnalyzer()
    tokenPos = []
    for word, tag in tagsDict:
        tStr = tag.replace(',', ' ')
        tList = tStr.split(' ')
        # a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
        # от части речи зависит, какие признаки отправляются в грамматику, отсюда условия
        a = morphAnalyz.parse(word)
        for y in a:  # y - объект, а - лист
            yStr = str(y.tag).replace(',', ' ')
            yTagList = yStr.split(' ')
            if sorted(tList) == sorted(yTagList):
                tokenPos.append(y)
    return tokenPos