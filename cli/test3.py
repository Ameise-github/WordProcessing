from pprint import pprint

import spacy_udpipe

from parsing.semantic.Models import Models
from parsing.text import Text

from gensim.matutils import jaccard



trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


def distance_metrics_Jaccard(text_standart, textsList):
    #Получить список лемм сех текстов
    data_lemmatized_list = []
    data_lemmatized_list.append(text_standart.lemma_text)
    for text in textsList:
        data_lemmatized_list.append(text.lemma_text)

    # Модель LDA для поиска темы в тексте текста
    models = Models()
    model_LDA = models.text_LDA(data_lemmatized_list)

    # Получить мешок слов
    bow_text_standart = model_LDA.id2word.doc2bow(text_standart.lemma_text)
    for text in textsList:
        bow_text = model_LDA.id2word.doc2bow(text.lemma_text)
        # print("jaccard [0 - подобны; 1 - не подобны]")
        # print(jaccard(bow_text_standart, bow_text))
        text.jaccard_coeff = round(jaccard(bow_text_standart, bow_text), 2)


def cosine_similarity(text_standart, textsList):
    # Получить список лемм сех текстов
    data_lemmatized_list = []
    data_lemmatized_list.append(text_standart.lemma_text)
    for text in textsList:
        data_lemmatized_list.append(text.lemma_text)

    models = Models()
    # Model LSI точно определяет подобие документов чем больше тем лучше, если = 1 то текста равны
    model_LSI, index = models.text_LSI(data_lemmatized_list)
    vec_text_standart = model_LSI.id2word.doc2bow(text_standart.lemma_text)
    vec_lsi_stand_text = model_LSI[vec_text_standart]  # преобразовать запрос в LSI
    sims = index[vec_lsi_stand_text]  # выполнить запрос сходства с корпусом
    # print("cos [1 - подобны; -1 - не подобны]")
    # print( list(enumerate(sims)))
    list_sims = list(enumerate(sims))
    for i, (n, c) in enumerate(list_sims[1::]):
        textsList[i].cos_sim = round(c, 2)



def main():
    textOriginalList = [textOriginal3, textOriginal2]
    # Преобразовать в объекты Text
    textsList = []
    for textOriginal in textOriginalList:
        textsList.append(Text(textOriginal))
    text_standart = Text(textOriginal1)
    # Модель для синтаксичского аналза
    nlp = spacy_udpipe.load_from_path(lang="ru",
                                      path=trainTextUdpipe,
                                      meta={"description": "Custom 'ru' model"})

    for text in textsList:
        # Получение синтаксической модели
        text.doc = nlp(' '.join(text.tokenz))
        # Получение леммы
        text.lemma_text = text.get_lemma_list(text.doc)

    text_standart.doc = nlp(' '.join(text_standart.tokenz))
    text_standart.lemma_text = text_standart.get_lemma_list(text_standart.doc)

    distance_metrics_Jaccard(text_standart, textsList)
    cosine_similarity(text_standart, textsList)
    print("!!!!")



if __name__ == '__main__':
    main()