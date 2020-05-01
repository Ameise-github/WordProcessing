import parsing.approximation_CT as approximation_CT
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis
from spacy.tokens import Doc


class Text:
    """
    Класс описания модели текста
    """
    def __init__(self, path_file):
        self.text_path: str = path_file
        self.tokenz: list = self.graphematic(text_path=self.text_path)
        self.doc: Doc = None
        self.matrix = None
        self.entropy: float = 0
        self.entropy2: float = 0
        self.entropy3: float = 0
        self.CT = approximation_CT.approximation_CT()
        self.freq_dist: dict = dict()
        self.lemma_text: list = list()
        self.p: float = 0.0
        self.jaccard_coeff: float = 0.0
        self.cos_sim: float = 1.0


    # Получение токенов
    def graphematic(self, text_path: str):
        # Инициализация графематического анализа. Передача в конструктор исходного текста
        graphemAnaliz = GraphematicAnalysis(text_path, punct=True)
        # разбиваем текст на токены
        textTokenzList = graphemAnaliz.get_sentences()
        return textTokenzList

     # Лемматизация слов
    def get_lemma_list(self, doc: Doc):
        """
        Лемматизация слов
        :param doc: полученный документ spacy модели
        :return: список лемм текста
        """
        lema_list = []
        for token in doc:
            lema_list.append(token.lemma_)
        return lema_list