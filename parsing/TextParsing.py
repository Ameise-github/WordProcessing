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

from parsing.syntax.syntax import SyntaxAnalysis

trainText = '../resource/data/trainText.tab'
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/grammarRU.fcfg"


def text_analysis(trainText, textOriginalList, pathToFileGrammer, morphAnalyzer):
    # Читаем подкорпус НКРЯ из файла с разделителем-табуляцией
    with open(trainText, encoding='utf-8') as f:
        sents = list(read_corpus_to_nltk(f))

    # Обучаем контекстный теггер на получившемся наборе предложений:
    contextTegger = PMContextTagger(train=sents, type_="full")

    # Инициализация графематического анализа. Передача в конструктор исходного текста
    graphemAnalizList = []
    for textOriginal in textOriginalList:
        graphemAnalizList.append(GraphematicAnalysis(textOriginal))

    # разбиваем текст на токены
    textTokenzList = []
    for graphemAnaliz in graphemAnalizList:
        textTokenzList.append(graphemAnaliz.get_sentences())

    # for index, token in enumerate(textTokenz):
    #     textTokenz[index] = str.lower(token)

    # Применим полученную модель морфологии к предложению
    tagsDictsList = []
    for textTokenz in textTokenzList:
        tagsDictsList.append(contextTegger.tag(textTokenz))

    # СИНТАКСИС
    #Вариант 1
    # region
    syntax_analis = SyntaxAnalysis(pathToFileGrammer)
    # Преобразование граматики из вида pymorphy в вид nltk и получение слов с разбором
    tokenPosList = []
    for tagsDict in tagsDictsList:
        tokenPosList.append(syntax_analis.pm2fcfg(tagsDict, pathToFileGrammer, morphAnalyzer))

    # Перевести строковое значение в значение URL
    url_path = Path(pathToFileGrammer).absolute().as_uri()
    # построить синтаксический анализатор
    cp = load_parser(url_path, trace=1)
    # Получить синтаксическое дерево
    # trees = cp.parse(textTokenz)
    # for tree in trees:
    #     tree.draw()
    #     pprint(tree)
    # endregion

    # Частота слов в тексте(получаем словарь слово-часота)
    freq_dist_lem_list = []
    for tokenPos in tokenPosList:
        freq_dist_lem_list.append(freq_dist_dic(tokenPos))

    # Пулучение списка лемм
    data_lemmatized_list = []
    for tokenPosL in tokenPosList:
        data_lemmatized_list.append(get_lemma_list(tokenPosL))

    # Модель LDA для поиска темы в тексте текста
    models = Models()
    model_LDA = models.text_LDA(data_lemmatized_list)

    # Сравнить первый документ(эталон) с другим(и)
    # Получить мешок слов
    bow_doc0 = model_LDA.id2word.doc2bow(data_lemmatized_list[0])
    for i in range(1, len(data_lemmatized_list)):
        bow_doc_tmp = model_LDA.id2word.doc2bow(data_lemmatized_list[i])
        # Сравнить документы по моделям LDA
        index_jaccard = jaccard(bow_doc0, bow_doc_tmp)
        # Если индекс не больше 0.6 (взяли с потолка) то ищем энтропию
        # if index_jaccard <= 0.6:
        # print("Документ под номером " + str(i) + " подходит. jaccard  = " + str(index_jaccard))

    # Или можно исолзовать этот способ, определяет подобие точно
    # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
    # model_LSI, index = models.text_LSI(data_lemmatized_list)
    # vec_doc1 = model_LSI.id2word.doc2bow(data_lemmatized_list[1])
    # vec_lsi = model_LSI[vec_doc1]  # convert the query to LSI space
    # sims = index[vec_lsi]  # выполнить запрос сходства с корпусом
    # print("LSI matrix")
    # pprint(list(enumerate(sims)))  # print (document_number, document_similarity) 2-tuples
    # Отсортировать в порядке убывания
    # sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # for i, s in enumerate(sims):
    #     print(s, textOriginalList[i])


    # return textTokenz, wfst1


# Частота слов в тексте
def freq_dist_dic(tokenPosList):
    # Поулчение лемм
    lema_list = get_lemma_list(tokenPosList)
    # Получение количество встречаемости слова
    freq_dist_pos = FreqDist(lema_list)
    # Получение частоты встречаемости слова(словарь)
    freq_dist_lem = {}
    for k, v in freq_dist_pos.items():
        freq_dist_lem[k] = v / len(freq_dist_pos)
    return freq_dist_lem


# Лемматизация слов
def get_lemma_list(tokenPosList):
    """
    Лемматизация слов
    :param tokenPosList: Лист токенов
    :return:
    """
    lema_list = []
    for token in tokenPosList:
        y_normal_form = str(token.normal_form).replace('ё', 'е')
        lema_list.append(y_normal_form)
    return lema_list


def main():
    morphAnalyzer = pymorphy2.MorphAnalyzer()
    textOriginalList = [textOriginal1, textOriginal2]
    text_analysis(trainText, textOriginalList, pathToFileGrammer, morphAnalyzer)


if __name__ == '__main__':
    main()
