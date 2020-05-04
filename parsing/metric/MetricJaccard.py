from parsing.metric.MetricAnalysis import MetricAnalysis
from parsing.semantic.Models import Models
from parsing.text import Text
from gensim.matutils import jaccard


class MetricJaccard(MetricAnalysis):
    def __init__(self, trainTextUdpipe):
        super().__init__(trainTextUdpipe)
        self.name = "Метрика Жаккарда"

    def run(self):
        """
        Вычисление метрики Jaccard
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(self._text_standart.lemma_text)
        data_lemmatized_list.append(self._text.lemma_text)

        # Модель LDA для поиска темы в тексте текста
        models = Models()
        model_LDA = models.text_LDA(data_lemmatized_list)

        # Получить мешок слов
        bow_text_standart = model_LDA.id2word.doc2bow(self._text_standart.lemma_text)
        bow_text = model_LDA.id2word.doc2bow(self._text.lemma_text)
        # print("jaccard [0 - подобны; 1 - не подобны]")
        # print(jaccard(bow_text_standart, bow_text))
        self._text.jaccard_coeff = round(jaccard(bow_text_standart, bow_text), 2)