# coding:utf8
from pprint import pprint
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from nltk import load_parser, FreqDist, parse
from parsing.syntax.MatrixSyntax import MatrixSyntax
import pymorphy2
from pathlib import Path
import nltk
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from parsing.syntax.syntax import MySyntax

trainText = '../resource/data/trainText.tab'
textOriginal1 = "../resource/data/text3.txt"
textOriginal2 = "../resource/data/text1.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/test.fcfg"


def text_analysis(trainText, textOriginalList, pathToFileGrammer, morphAnalyzer):
    # Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
    with open(trainText, encoding='utf-8') as f:
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
    # Преобразование граматики из вида pymorphy в вид nltk и получение слов с разбором
    tokenPosList = mySyntax.pm2fcfg(tagsDict, pathToFileGrammer, morphAnalyzer)
    # Перевести строковое значение в значение URL
    url_path = Path(pathToFileGrammer).absolute().as_uri()
    # построить синтаксический анализатор
    # cp = load_parser(url_path, trace=1)
    # Получить синтаксическое дерево
    # trees = cp.parse(textTokenz)
    # for tree in trees:
    #     tree.draw()
    #     pprint(tree)

    # Частота слов в тексте
    freq_dist_lem = freq_dist_dic(tokenPosList)
    print(freq_dist_lem)

    # Получение матрицы синтаксического дерева. ПО статье хабра получение матрицы WFST
    # grammar = cp.grammar()
    # grammar.productions()
    # matrixSyntax = MatrixSyntax()
    # wfst0 = matrixSyntax.init_wfst(textTokenz, grammar)
    # wfst1 = matrixSyntax.complete_wfst(wfst0, textTokenz, grammar)
    # matrixSyntax.display(wfst0, textTokenz)

    #Тема текста
    theme_text(textTokenz, tokenPosList)

    # return textTokenz, wfst1

#Частота слов в тексте
def freq_dist_dic(tokenPosList):
    #Поулчение лемм
    lema_list = get_lema_list(tokenPosList)
    #Получение количество встречаемости слова
    freq_dist_pos = FreqDist(lema_list)
    #Получение частоты встречаемости слова
    freq_dist_lem = {}
    for k, v in freq_dist_pos.items():
        freq_dist_lem[k] = v / len(freq_dist_pos)
    return freq_dist_lem

#Тема текстов
def theme_text(data_words_tokens, tokenPosList):
    """
    Определение темы текстов
    :param data_words_tokens: токены из текта
    :return:
    """
    #Модель для получения биграмм и триграмм
    bigram = gensim.models.Phrases(data_words_tokens, min_count=3, threshold=50)  # выше threshold .
    trigram = gensim.models.Phrases(bigram[data_words_tokens], threshold=50)
    #Более быстрый способ получить предложение, разабитое как триграмма / биграмма
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    #Получение биграмм
    data_words_bigrams = make_bigrams(docs, bigram_mod)

    ##TODO необходимо сделать работу со множеством файлов и везде передавать множество документов, иначе не построить корпус

    #Пулучение лемм
    data_lemmatized = get_lema_list(tokenPosList)
    #Создание словаря
    id2word = corpora.Dictionary(data_lemmatized)
    # Создание корпуса
    texts = data_lemmatized
    # Частота слов в документе
    corpus = [id2word.doc2bow(text) for text in texts]

    #Вывод
    print(trigram_mod[bigram_mod[data_words_tokens]])
    print(corpus[:1])


#Получение биграмм
def make_bigrams(docs, bigram_mod):
    return [bigram_mod[doc] for doc in docs]


#Получение триграмм
def make_trigrams(docs, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in docs]


#Лемматизация слов
def get_lema_list(tokenPosList):
    lema_list = []
    for token in tokenPosList:
        lema_list.append(token.normal_form)
    return lema_list

def main():
    morphAnalyzer = pymorphy2.MorphAnalyzer()
    text_analysis(textMedia, textOriginal, pathToFileGrammer, morphAnalyzer)


if __name__ == '__main__':
    main()

