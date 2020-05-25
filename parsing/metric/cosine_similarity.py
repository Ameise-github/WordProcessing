from parsing.metric.base import BaseAlgorithm
from parsing.semantic.Models import Models
from parsing.text import Text


class CosineSimilarityAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "Косинусное сходство"

    def process(self, udpipe: str, reference: str, other: str) -> float:
        # init
        reference_text = Text(reference, udpipe)
        other_text = Text(other, udpipe)

        # Получить список лемм всех текстов
        data_lemmatized_list = [
            reference_text.lemma_text,
            other_text.lemma_text
        ]

        # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
        models = Models()
        model_LSI, index = models.text_LSI(data_lemmatized_list)
        vec_reference = model_LSI.id2word.doc2bow(reference_text.lemma_text)
        vec_lsi_reference = model_LSI[vec_reference]  # преобразовать запрос в LSI
        sims = index[vec_lsi_reference]  # выполнить запрос сходства с корпусом
        # print("cos [1 - подобны; -1 - не подобны]")
        # print( list(enumerate(sims)))
        list_sims = list(enumerate(sims))
        for i, (n, c) in enumerate(list_sims[1::]):
            other_text.cos_sim = round(c, 2)

        return other_text.cos_sim
