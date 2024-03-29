# coding:utf8
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
import pymorphy2
from parsing.text import Text
from spacy import displacy


class TextAnalysis:
    """
    Класс текстового анализа.
    Включает в себя морфологию и синтаксис
    """

    # Морфологический анализ текста
    def morph_analysis(self, trainTextNLTK4russian, textOriginal, rusTag=False):
        """
        Морфологический анализ текста
        :param trainTextNLTK4russian: текст с табцляциями для тренировки модели
        :param textOriginal: путь к файлу с текстом
        :return: список tag pymorphy
        """
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

        tokenPosList = self.get_tag_pymorphy(tagsDict)
        tokenList =[]
        for token in tokenPosList:
            if rusTag:
                tokenTag = str(token.tag.cyr_repr)
            else:
                tokenTag = str(token.tag)
            tokenTag = tokenTag.replace(" ", ",")
            ind = tokenTag.find(',')
            tmp = [token.word, token.normal_form, tokenTag[0: ind], tokenTag[ind + 1 :]]
            tokenList.append(tmp)
        return tokenList

    # Получить tag как объект pymorphy2
    def get_tag_pymorphy(self, tagsDict):
        """
        Получить tag как объект pymorphy2
        :param tagsDict: словарь [слово-морфологический признаки]
        :return: список tag
        """
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

    # Отображение синтаксического дерева
    def view_syntax_tree(self, pathText, trainTextUdpipe):
        """
        Отрисовка синтаксического дерева
        :param pathText: пусть к тексту
        :param trainTextUdpipe: Модель для тренировки синтаксичского аналза
        :return: html представление дерева
        """
        text_tmp = Text(pathText,trainTextUdpipe)
        html_trees = displacy.render(text_tmp.doc, style="dep")
        return html_trees