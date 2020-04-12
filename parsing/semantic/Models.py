# Gensim
from gensim import similarities, models
import gensim.corpora as corpora
from collections import defaultdict
# Визуализация модели LDA
import pyLDAvis
import pyLDAvis.gensim



class Models:
    # Тема текстов метод LDA
    def text_LDA(self, data_words_tokens, data_lemmatized_list):
        """
        Определение темы текстов
        сайт https://radimrehurek.com/gensim/auto_examples/tutorials/run_distance_metrics.html#sphx-glr-auto-examples-tutorials-run-distance-metrics-py
        :param data_words_tokens: лист токенов из тектов
        :param data_lemmatized_list: лист лемм всех документов
        :return:
        """
        # Модель для получения биграмм и триграмм
        bigram = models.Phrases(data_words_tokens, min_count=10, threshold=100)  # выше threshold .
        trigram = models.Phrases(bigram[data_words_tokens], threshold=100)
        # Более быстрый способ получить предложение, разабитое как триграмма / биграмма
        bigram_mod = models.phrases.Phraser(bigram)
        trigram_mod = models.phrases.Phraser(trigram)
        # Получение биграмм
        data_words_bigrams = self.make_bigrams(data_words_tokens, bigram_mod)

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
            # num_topics = len(data_words_tokens),
        lda_model = models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=len(data_words_tokens),
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=50,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        # Вывод для проверки
        # Читаемый человеком формат корпуса (термин-частота)
        # print([[(id2word[id], freq) for id, freq in cp] for cp in corpus])
        # ключевые слова для каждой темы и вес (важность) каждого ключевого слова
        # print("lda_model")
        # pprint(lda_model.print_topics())
        # Визуализация модели LDA
        # vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
        # pyLDAvis.save_html(vis, 'LDA_Visualization.html')

        return lda_model

    # модель LSI
    def text_LSI(self, data_lemmatized_list):
        #https://radimrehurek.com/gensim/auto_examples/core/run_similarity_queries.html
        # remove words that appear only once
        frequency = defaultdict(int)
        for text in data_lemmatized_list:
            for token in text:
                frequency[token] += 1

        texts = [
            [token for token in text if frequency[token] > 1]
            for text in data_lemmatized_list
        ]

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
        index = similarities.MatrixSimilarity(lsi[corpus])
        return lsi, index


    # Получение биграмм
    def make_bigrams(self, docsTokenList, bigram_mod):
        return [bigram_mod[docToken] for docToken in docsTokenList]


    # Получение триграмм
    def make_trigrams(self, docs, bigram_mod, trigram_mod):
        return [trigram_mod[bigram_mod[doc]] for doc in docs]