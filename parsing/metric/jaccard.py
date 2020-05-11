from parsing.metric.base import BaseAlgorithm
from parsing.semantic.Models import Models
from parsing.text import Text
from gensim.matutils import jaccard


class JaccardAlgorithm(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "Метрика Жаккарда"

    def process(self, udpipe: str, reference: str, other: str):
        # init
        reference_text = Text(reference, udpipe)
        other_text = Text(other, udpipe)

        # Получить список лемм всех текстов
        data_lemmatized_list = [
            reference_text.lemma_text,
            other_text.lemma_text
        ]

        # Модель LDA для поиска темы в тексте текста
        models = Models()
        model_LDA = models.text_LDA(data_lemmatized_list)

        # Получить мешок слов
        bow_reference = model_LDA.id2word.doc2bow(reference_text.lemma_text)
        bow_other = model_LDA.id2word.doc2bow(other_text.lemma_text)
        # print("jaccard [0 - подобны; 1 - не подобны]")
        # print(jaccard(bow_text_standart, bow_text))
        other_text.jaccard_coeff = round(jaccard(bow_reference, bow_other), 2)

        return other_text.p
