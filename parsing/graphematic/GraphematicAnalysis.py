import string
from collections import Counter

import parsing.graphematic.Porter as porter
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


#  nltk.download()  #раскоментировать и загрузить всю библиотеку

class GraphematicAnalysis:
    """
    Класс для проведения графематического анализа

    Attributes
    ----------
    path : str
        путь к целевому файлу

    Methods
    -------
    __init_collection(path)
        Приватный метод первоначального инициализирования объекта.

    __tokenize_ru(sent):
        Приватный метод разбиения предложения на слова.

    get_most_common_phrase_stemmed(limit, file_path=None):
        Метод получения самых используемых словосочетаний со стеммингом

    get_most_common_phrase_non_stemmeed(limit, file_path=None):
        Метод получения самых используемых словосочетаний без стемминга

    get_sentences(file_path=None):
        Метод получения массива предложений разбитых на слова
    """

    def __init__(self, path):
        self.__phrase_counters = None
        self.__sentences = None
        self.path = path
        self.__init_collection(path)

    def __init_collection(self, path):
        """Приватный метод первоначального инициализирования объекта.

        Parameters
        ----------
        Токенизирует текст и разбивает его на предложения, а потом и на слова.
         :param path: str
            путь к целевому файлу
        """
        try:
            text = open(path, 'r', encoding='utf-8').read()
        except FileNotFoundError:
            print("Файл не найден")
            return -1
        # text_new = ""
        # prev_char = ""
        # for idx, char in enumerate(text):  # замена всех слов, которые могут быть инициалама на ничто.
        #     if prev_char.isupper() and char == ".":
        #         char = ""
        #     prev_char = char
        #     text_new = text_new + char

        self.__phrase_counters = Counter()
        # разбиваем текст на предложения, а их разбиваем на слова испольхуя функцию  tokenize_ru
        self.__sentences = self.__tokenize_ru(text.lower())

    def __tokenize_ru(self, sent):
        """Приватный метод разбиения предложения на слова.

        Parameters
        ----------
        Разбивает предложение на слова, добавляя новые исключеиня и убирая "мусор"
        :param sent: tuple
            предложение для разбиения

        Returns
        -------
        :return tuple
            разбитое на слова предложение
        """
        tokens = word_tokenize(sent, language="russian")
        tokens = [i for i in tokens if (i not in string.punctuation)]

        stop_words = stopwords.words('russian')
        # добавляем в список исключаемых слов новые
        stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', '—', '–', 'к', 'на',
                           '...', 'т.д.', 'т.д', 'т.к.', 'которые', 'которых', 'твой', 'которой', 'которого', 'сих',
                           'ком', 'свой', 'твоя', 'этими', 'слишком', 'нами', 'всему', 'будь', 'саму', 'чаще', 'ваше',
                           'сами', 'наш', 'затем', 'еще', 'самих', 'наши', 'ту', 'каждое', 'мочь',
                           'весь', 'этим', 'наша', 'своих', 'оба', 'который', 'зато', 'те', 'этих', 'вся', 'ваш',
                           'такая', 'теми', 'ею', 'которая', 'нередко', 'каждая', 'также', 'чему', 'собой', 'самими',
                           'нем', 'вами', 'ими', 'откуда', 'такие', 'тому', 'та', 'очень', 'сама', 'нему', 'алло',
                           'оно', 'этому', 'кому', 'тобой', 'таки', 'твое', 'каждые', 'твои', 'мой', 'нею', 'самим',
                           'ваши', 'ваша', 'кем', 'мои', 'однако', 'сразу', 'свое', 'ними', 'всё', 'неё', 'тех', 'хотя',
                           'всем', 'тобою', 'тебе', 'одной', 'другие', 'эта', 'само', 'эта', 'буду', 'самой', 'моё',
                           'своей', 'такое', 'всею', 'будут', 'своего', 'кого', 'свои', 'мог', 'нам', 'особенно', 'её',
                           'ee', 'самому', 'наше', 'кроме', 'вообще', 'вон', 'мною', 'никто',
                           ])

        tokens = [i for i in tokens if (i not in stop_words)]
        tokens = [i.replace("«", "").replace("»", "").replace("\'\'", "").replace("``", "") for i in tokens]
        for i in tokens:
            if i == "":
                tokens.remove(i)
        return tokens

    def get_most_common_phrase_stemmed(self, limit, file_path=None):
        """Метод получения самых используемых словосочетаний со стеммингом

        Parameters
        ----------
        :param limit: int
            максимальная длина словосочетания
        :param file_path: str, optional
            путь к файлу для вывода

        Returns
        -------
        :return tuple
             самые выстречаемые словосочетания
        """
        if file_path:
            try:
                file = open(file_path, 'w', encoding='utf-8')
            except FileNotFoundError:
                print("Файл не найден")
                return -1
            stemmed = self.__sentences  # стеммеинг
            for idx, sent in enumerate(self.__sentences):
                for jdx, word in enumerate(sent):
                    stemmed[idx][jdx] = porter.Porter.stem(word)

            for i in range(2, limit):  # находим самые встречаемые словосочентания делая пары из всех 2-6 слов
                for sent in stemmed:
                    for phrase in ngrams(sent, i):
                        self.__phrase_counters[phrase] += 1
            most_common_all = self.__phrase_counters.most_common()  # перевод самых встречаемых в массиве phrase_counters в most_common_all
            for element in most_common_all:
                final_str = " ".join(element[0])
                final_str = final_str + ", " + str(element[1]) + "\n"
                file.write(final_str)
            file.close()
            return 0
        else:
            stemmed = self.__sentences  # стеммеинг
            for idx, sent in enumerate(self.__sentences):
                for jdx, word in enumerate(sent):
                    stemmed[idx][jdx] = porter.Porter.stem(word)

            for i in range(2, limit):  # находим самые встречаемые словосочентания делая пары из всех 2-6 слов
                for sent in stemmed:
                    for phrase in ngrams(sent, i):
                        self.__phrase_counters[phrase] += 1

            most_common_all = self.__phrase_counters.most_common()  # перевод самых встречаемых в массиве phrase_counters в most_common_all

            return most_common_all

    def get_most_common_phrase_non_stemmeed(self, limit, file_path=None):
        """Метод получения самых используемых словосочетаний без стемминга

        Parameters
        ----------
        :param limit: int
            максимальная длина словосочетания
        :param file_path: str, optional
            путь к файлу для вывода

        Returns
        -------
        :return tuple
             самые выстречаемые словосочетания
        """
        if file_path:
            try:
                file = open(file_path, 'w', encoding='utf-8')
            except FileNotFoundError:
                print("Файл не найден")
                return -1
            for i in range(2, limit):  # находим самые встречаемые словосочентания делая пары из всех 2-6 слов
                for sent in self.__sentences:
                    for phrase in ngrams(sent, i):
                        self.__phrase_counters[phrase] += 1

            most_common_all = self.__phrase_counters.most_common()  # перевод самых встречаемых в массиве phrase_counters в most_common_all

            for element in most_common_all:
                final_str = " ".join(element[0])
                final_str = final_str + ", " + str(element[1]) + "\n"
                file.write(final_str)
            file.close()
            return 0
        else:
            for i in range(2, limit):  # находим самые встречаемые словосочентания делая пары из всех 2-6 слов
                for sent in self.__sentences:
                    for phrase in ngrams(sent, i):
                        self.__phrase_counters[phrase] += 1

            most_common_all = self.__phrase_counters.most_common()  # перевод самых встречаемых в массиве phrase_counters в most_common_all

            return most_common_all

    def get_sentences(self, file_path=None):
        """Метод получения массива предложений разбитых на слова

        Parameters
        ----------
        :param file_path: str, optional
            путь к файлу для вывода

        Returns
        -------
        :return tuple
            Массив преложений разбитых на слова
        """

        if file_path:
            try:
                file = open(file_path, 'w', encoding='utf-8')
            except FileNotFoundError:
                print("Файл не найден")
                return -1
            for element in self.__sentences:
                file.write(", ".join(element) + "\n")
            file.close()
            return 0
        else:
            return self.__sentences
