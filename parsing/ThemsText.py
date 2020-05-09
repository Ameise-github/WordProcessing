from parsing.semantic.Models import Models
from parsing.text import Text


class ThemsText:
    def __init__(self, list_path_text, pathTrainTextUdpipe, optimal_topics=False):
        self.optimal_topics = optimal_topics
        self.list_path_text = list_path_text
        self.trainTextUdpipe = pathTrainTextUdpipe
        self._data_lemmatized_list = None
        self.list_texts = None
        self.model = Models()

    def view_thems(self):
        list_text = []
        for tp in self.list_path_text:
            list_text.append(Text(tp, self.trainTextUdpipe))
        # Получить список лемм всех текстов
        data_lemmatized_list = []
        for text in list_text:
            data_lemmatized_list.append(text.lemma_text)

        self._data_lemmatized_list = data_lemmatized_list
        self.list_texts = list_text

        view_srt, lda_model = self.model.view_topic_LDA(data_lemmatized_list, self.optimal_topics)
        return view_srt, lda_model

    def topics_document(self, lda_model):
        return self.model.format_topics_sentences(lda_model, self._data_lemmatized_list, self.list_texts)
