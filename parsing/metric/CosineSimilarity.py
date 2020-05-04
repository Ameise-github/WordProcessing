from parsing.metric.MetricAnalysis import MetricAnalysis
from parsing.semantic.Models import Models
from parsing.text import Text


class CosineSimilarity(MetricAnalysis):
    def __init__(self, trainTextUdpipe):
        super().__init__(trainTextUdpipe)
        self.name = "Косинусное сходство"

    def run(self):
        """
        Вычисление косинусное сходства документов
        :param text_standart: текст эталон (Объект Text)
        :param text: сравниваемый текст (бъект Text)
        :return:
        """
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        data_lemmatized_list.append(self._text_standart.lemma_text)
        data_lemmatized_list.append(self._text.lemma_text)

        # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
        models = Models()
        model_LSI, index = models.text_LSI(data_lemmatized_list)
        vec_text_standart = model_LSI.id2word.doc2bow(self._text_standart.lemma_text)
        vec_lsi_stand_text = model_LSI[vec_text_standart]  # преобразовать запрос в LSI
        sims = index[vec_lsi_stand_text]  # выполнить запрос сходства с корпусом
        # print("cos [1 - подобны; -1 - не подобны]")
        # print( list(enumerate(sims)))
        list_sims = list(enumerate(sims))
        for i, (n, c) in enumerate(list_sims[1::]):
            self._text.cos_sim = round(c, 2)
