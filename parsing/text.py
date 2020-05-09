from parsing.approximation_CT import approximation_CT
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from spacy.tokens import Doc
import numpy
from nltk import FreqDist
# spacy
from spacy.tokens import Doc
import spacy_udpipe

class Text:
    """
    Класс описания модели текста
    """
    def __init__(self, path_file, trainTextUdpipe):
        # Модель для синтаксичского аналза
        self.nlp = spacy_udpipe.load_from_path(lang="ru",
                                               path=trainTextUdpipe,
                                               meta={"description": "Custom 'ru' model"})
        self.text_path: str = path_file
        self.tokenz: list = self.graphematic()
        # Получение синтаксической модели
        self.doc: Doc = self.nlp(' '.join(self.tokenz))
        # Получение леммы
        self.lemma_text: list = self.get_lemma_list()
        # Получение частоты
        self.freq_dist: dict = dict()
        # Получение матрицы вероятности
        self.matrix = None
        self.entropy: float = 0.0
        self.entropy2: float = 0.0
        self.entropy3: float = 0.0
        self.CT = None
        self.p: float = 1.0
        self.jaccard_coeff: float = 0.0
        self.cos_sim: float = 1.0

    # Получение токенов
    def graphematic(self):
        # Инициализация графематического анализа. Передача в конструктор исходного текста
        graphemAnaliz = GraphematicAnalysis(self.text_path)
        # разбиваем текст на токены
        textTokenzList = graphemAnaliz.get_sentences()
        return textTokenzList

    # Лемматизация слов
    def get_lemma_list(self):
        """
        Лемматизация слов
        :return: список лемм текста
        """
        lema_list = []
        for token in self.doc:
            lema_list.append(token.lemma_)
        return lema_list

    # Вероятность слов в тексте
    def freq_dist_dic(self):
        """
        Вероятность слов в тексте
        :param lema_list: список лемм текста
        :return: словарь [слово-вероятность]
        """
        # Получение количество встречаемости слова
        freq_dist_pos = FreqDist(self.lemma_text)
        # Получение частоты встречаемости слова(словарь)
        freq_dist_lem = {}
        for k, v in freq_dist_pos.items():
            freq_dist_lem[k] = v / len(freq_dist_pos)
        # return freq_dist_lem
        self.freq_dist = freq_dist_lem

    # Вычисление энтропии
    def get_entropy(self):
        """
        Вычисление энтропии
        :param matrix_probability: матрица вероятности
        :param entropy2: для рассчета 2-ого начального момента энтропии
        :param entropy3: для рассчета 3-ого начального момента энтропии
        :return: значение энтропии
        """
        s = 0
        s2 = 0
        s3 = 0
        for row in self.matrix:
            for elem in row:
                if (elem != 0):
                        s2 += numpy.power(elem, 2) * numpy.log2(elem)
                        s3 += numpy.power(elem, 3) * numpy.log2(elem)
                        s += elem * numpy.log2(elem)
        # return -s
        self.entropy2 = -s2
        self.entropy3 = -s3
        self.entropy = -s

    # Получение матрицы
    def matrix_syntax(self):
        """
        Получение вероятностной матрицы
        :param doc: документ полученный из spacy модели
        :freq_dist_lem dict: словарь лемм текста
        :return: матрица ероятности
        """
        n = len(self.doc)
        matrix = numpy.zeros((n, n), dtype=float)
        for token in self.doc:
            for child in token.children:
                pi1 = self.freq_dist[token.lemma_]
                pi2 = self.freq_dist[child.lemma_]
                matrix[token.i][child.i] = 1 * pi1 * pi2
        # return matrix
        self.matrix = matrix