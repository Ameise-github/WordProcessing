# Gensim
from pprint import pprint

from gensim import similarities, models
import gensim.corpora as corpora
from collections import defaultdict

from gensim.models import CoherenceModel
from gensim.models.ldamulticore import LdaMulticore
# Визуализация модели LDA
import pyLDAvis
import pyLDAvis.gensim

import numpy as np


class Models:
    # Тема текстов метод LDA
    def text_LDA(self, data_lemmatized_list, optimal_topics=False):
        """
        Определение темы текстов
        сайт https://radimrehurek.com/gensim/auto_examples/tutorials/run_distance_metrics.html#sphx-glr-auto-examples-tutorials-run-distance-metrics-py
        :param data_lemmatized_list: лист лемм всех документов
        :return:
        """
        #формирование словваря и корпуса
        id2word, corpus = self.get_corpus_dictionary(data_lemmatized_list)

        if optimal_topics:
            # Вызовем функцию и посчитаем оптимальное количество тем
            model_list, coherence_values = self.compute_coherence_values(dictionary=id2word, corpus=corpus,
                                                                         texts=data_lemmatized_list,
                                                                         start=len(data_lemmatized_list), limit=35,
                                                                         step=len(data_lemmatized_list))
            ind_lda = coherence_values.index(max(coherence_values))
            lda_model = model_list[ind_lda]
        else:
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
                                                 num_topics=len(data_lemmatized_list),
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
        # pprint(lda_model.print_topics())

        return lda_model

    # модель LSI
    def text_LSI(self, data_lemmatized_list):
        """
        Получение модели LSI и index_matrix
        :param data_lemmatized_list: список лемм всех текстов
        :return:
        """
        # https://radimrehurek.com/gensim/auto_examples/core/run_similarity_queries.html
        # удалить слова, которые появляются только один раз
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
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=len(data_lemmatized_list))
        index = similarities.MatrixSimilarity(lsi[corpus])
        return lsi, index

    # Формирование словаря и корпуса
    def get_corpus_dictionary(self, data_lemmatized_list):
        """
        Формирование словаря и корпуса (id2word,corpus)
        :param data_lemmatized_list: список демм текстов
        :return: (id2word,corpus)
        """
        # Модель для получения биграмм и триграмм
        bigram = models.Phrases(data_lemmatized_list, min_count=10, threshold=100)  # выше threshold .
        trigram = models.Phrases(bigram[data_lemmatized_list], threshold=100)
        for idx in range(len(data_lemmatized_list)):
            for token in bigram[data_lemmatized_list[idx]]:
                if '_' in token:
                    # Токен это биграмма, добавим в документ.
                    data_lemmatized_list[idx].append(token)
            for token in trigram[data_lemmatized_list[idx]]:
                if '_' in token:
                    # Токен это три грамма, добавим в документ.
                    data_lemmatized_list[idx].append(token)

            # Создание словаря
        id2word = corpora.Dictionary(data_lemmatized_list)
        # Создание корпуса
        # Частота слов в документах
        corpus = [id2word.doc2bow(text) for text in data_lemmatized_list]
        return id2word, corpus

    # Визуализация тематики (модели LDA)
    def view_topic_LDA(self, data_lemmatized_list, optimal_topics=False):
        """
        Визуализация тематики (модели LDA)
        :param lda_model: модель LDA
        :param corpus: корпус слов
        :param id2word: словарь
        :param name_file: наименование файла для сохранения
        :return: строка html
        """
        #Получить модель LDA
        lda_model = self.text_LDA(data_lemmatized_list, optimal_topics)
        # Получить корпус и словарь
        id2word, corpus = self.get_corpus_dictionary(data_lemmatized_list)
        # Визуализация модели LDA
        # vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
        # pyLDAvis.save_html(vis, 'LDA_Visualization.html')
        vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
        #Сохранить в html
        # pyLDAvis.save_html(vis, name_file)
        # Вывод html
        vis_srt = pyLDAvis.prepared_data_to_html(vis)
        return vis_srt, lda_model

    def compute_coherence_values(self, dictionary, corpus, texts, limit, start=2, step=3):
        """
        Подсчет c_v когерентности для различного количества тем
        dictionary : Gensim словарь
        corpus : Gensim корпус
        texts : Список текста
        limit : Максимальное количество тем

        model_list : Список LDA моделей
        coherence_values :Когерентности, соответствующие модели LDA с количеством тем
        """
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())
        return model_list, coherence_values

    # отображает доминирующую тему и ее процентный вклад в каждом документе
    def format_topics_sentences(self, ldamodel, data_lemmatized_list, textsList):
        """
        Выводит доминирующую тему каждого текста
        :param ldamodel: LDA model
        :param data_lemmatized_list: список лемм всех текстов
        :param textsList: список объектов типа Text
        :return: список (номер темы, вес темы для этого текста, ключевые слова, объект Text)
        """
        id2word, corpus = self.get_corpus_dictionary(data_lemmatized_list)
        # инициализация выходной информации
        sent_topics_df = []
        # Получить основную тему в каждом документе
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Получить доминантную тему, Perc Contribution и ключевые слова для каждого документа
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    s_tmp = [int(topic_num), round(prop_topic, 4), topic_keywords, textsList[i].text_path]
                    sent_topics_df.append(s_tmp)
                else:
                    break
        return sent_topics_df
