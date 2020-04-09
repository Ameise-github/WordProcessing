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
# Визуализация модели LDA
import pyLDAvis
import pyLDAvis.gensim

from parsing.syntax.syntax import MySyntax

trainText = '../resource/data/trainText.tab'
textOriginal1 = "../resource/data/text3.txt"
textOriginal2 = "../resource/data/text1.txt"
textOriginal3 = "../resource/data/text2.txt"
textOut = "../resource/data/test_output.txt"
pathToFileGrammer = "../resource/book_grammars/test.fcfg"


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
    mySyntax = MySyntax(pathToFileGrammer)
    # Преобразование граматики из вида pymorphy в вид nltk и получение слов с разбором
    tokenPosList = []
    for tagsDict in tagsDictsList:
        tokenPosList.append(mySyntax.pm2fcfg(tagsDict, pathToFileGrammer, morphAnalyzer))

    # Перевести строковое значение в значение URL
    url_path = Path(pathToFileGrammer).absolute().as_uri()
    # построить синтаксический анализатор
    # cp = load_parser(url_path, trace=1)
    # Получить синтаксическое дерево
    # trees = cp.parse(textTokenz)
    # for tree in trees:
    #     tree.draw()
    #     pprint(tree)

    # Частота слов в тексте(получаем словарь слово-часота)
    freq_dist_lem_list = []
    for tokenPos in tokenPosList:
        freq_dist_lem_list.append(freq_dist_dic(tokenPos))

    # Получение матрицы синтаксического дерева. ПО статье хабра получение матрицы WFST
    # grammar = cp.grammar()
    # grammar.productions()
    # matrixSyntax = MatrixSyntax()
    # wfst0 = matrixSyntax.init_wfst(textTokenz, grammar)
    # wfst1 = matrixSyntax.complete_wfst(wfst0, textTokenz, grammar)
    # matrixSyntax.display(wfst0, textTokenz)

    # Тема текста
    theme_text_LDA(textTokenzList, tokenPosList)

    # return textTokenz, wfst1


# Частота слов в тексте
def freq_dist_dic(tokenPosList):
    # Поулчение лемм
    lema_list = get_lema_list(tokenPosList)
    # Получение количество встречаемости слова
    freq_dist_pos = FreqDist(lema_list)
    # Получение частоты встречаемости слова(слловарь)
    freq_dist_lem = {}
    for k, v in freq_dist_pos.items():
        freq_dist_lem[k] = v / len(freq_dist_pos)
    return freq_dist_lem


# Тема текстов метод LDA
def theme_text_LDA(data_words_tokens, tokenPosList):
    """
    Определение темы текстов
    :param data_words_tokens: лист токенов из тектов
    :return:
    """
    # Модель для получения биграмм и триграмм
    bigram = gensim.models.Phrases(data_words_tokens, min_count=10, threshold=100)  # выше threshold .
    trigram = gensim.models.Phrases(bigram[data_words_tokens], threshold=100)
    # Более быстрый способ получить предложение, разабитое как триграмма / биграмма
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    # Получение биграмм
    data_words_bigrams = make_bigrams(data_words_tokens, bigram_mod)

    # Пулучение списка лемм
    data_lemmatized_list = []
    for tokenPosL in tokenPosList:
        data_lemmatized_list.append(get_lema_list(tokenPosL))

    # Создание словаря
    id2word = corpora.Dictionary(data_lemmatized_list)
    # Создание корпуса
    # Частота слов в документах
    corpus = [id2word.doc2bow(text) for text in data_lemmatized_list]
    # Построение LDA модели
    # num_topics = количество запрошенных скрытых тем, которые нужно извлечь из учебного корпуса.
    # random_state = 100,
    # update_every = 1, количество документов, которые будут повторяться для каждого обновления
    # chunksize = 100, это количество документов, которые будут использоваться в каждом обучающем чанке
    # passes = 10, общее количество проходов обучения
    # alpha = 'auto', гиперпараметр, которые влияют на разреженность тем
    # per_word_topics = True модель вычисляет список тем, отсортированных в порядке убывания наиболее вероятных тем для каждого слова, вместе с их значениями ph, умноженными на длину элемента (то есть количество слов).
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=len(data_words_tokens),
                                                random_state=100,
                                                update_every=1,
                                                chunksize=50,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
    # Доминирующая тема в тексте
    dom_topics = format_topics_sentences(lda_model, corpus)

    # Вывод
    # Читаемый человеком формат корпуса (термин-частота)
    # print([[(id2word[id], freq) for id, freq in cp] for cp in corpus])
    # ключевые слова для каждой темы и вес (важность) каждого ключевого слова
    # print(lda_model.print_topics())
    # Визуализация модели LDA
    # vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    # pyLDAvis.save_html(vis, 'LDA_Visualization.html')

    print(dom_topics)
    return lda_model


# Поиск доминирующей темы в документе
def format_topics_sentences(ldamodel, corpus, texts_docs=None):
    #TODO спросить у Вани про sorted
    sent_topics = []
    # Получить основную тему в каждом документе
    for i, row in enumerate(ldamodel[corpus]):
        # Сортируем в порядке убывания
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Получить Perc Contribution and ключевые слова(Keywords) для каждого документа
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => доминирующая тема
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                s = [int(topic_num), round(prop_topic, 4), topic_keywords]
                sent_topics.append(s)
            else:
                break
    return sent_topics


# Получение биграмм
def make_bigrams(docsTokenList, bigram_mod):
    return [bigram_mod[docToken] for docToken in docsTokenList]


# Получение триграмм
def make_trigrams(docs, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in docs]


# Лемматизация слов
def get_lema_list(tokenPosList):
    """
    Лемматизация слов
    :param tokenPosList: Лист токенов
    :return:
    """
    lema_list = []
    for token in tokenPosList:
        lema_list.append(token.normal_form)
    return lema_list


def main():
    morphAnalyzer = pymorphy2.MorphAnalyzer()
    textOriginalList = [textOriginal1, textOriginal2, textOriginal3]
    text_analysis(trainText, textOriginalList, pathToFileGrammer, morphAnalyzer)


if __name__ == '__main__':
    main()
