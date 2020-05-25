from pprint import pprint

import nltk
from spacy import displacy

from parsing.ThemsText import ThemsText
from parsing.metric.cosine_similarity import CosineSimilarityAlgorithm
from parsing.metric.base import BaseAlgorithm
from parsing.metric.jaccard import JaccardAlgorithm
from parsing.metric.pragmatic_adequacy import PragmaticAdequacyAlgorithm
from parsing.metric.stochastic import StochasticAlgorithm
from parsing.text import Text
from parsing.semantic.Models import Models

from parsing.TextAnalysis import TextAnalysis
import spacy_udpipe

trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
trainTextNLTK4russian = '../resource/data/trainText.tab'
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text2.txt"
textOriginal3 = "../resource/data/text3.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


def main():
    # nltk.download('punkt')
    # nltk.download('stopwords')

    s = StochasticAlgorithm()
    res = s.process(trainTextUdpipe, textOriginal1, textOriginal2)
    res1 = s.process(trainTextUdpipe, textOriginal1, textOriginal3)
    print("StochasticAlgorithm:  " + str(res) + "; " + str(res1))

    c = CosineSimilarityAlgorithm()
    res2 = c.process(trainTextUdpipe, textOriginal1, textOriginal2)
    res3 = c.process(trainTextUdpipe, textOriginal1, textOriginal3)
    print("CosineSimilarityAlgorithm:  " + str(res2) + "; " + str(res3))

    j = JaccardAlgorithm()
    res4 = j.process(trainTextUdpipe, textOriginal1, textOriginal2)
    res5 = j.process(trainTextUdpipe, textOriginal1, textOriginal3)
    print("JaccardAlgorithm:  " + str(res4) + "; " + str(res5))

    # Изменения одного текста
    # one_text = PragmaticAdequacy()
    # one_text.set_trainTextUdpipe(trainTextUdpipe)
    # one_text.set_text_standart(textOriginal1)
    # one_text.set_text(textOriginal3)
    # print(one_text.run())

    # Тематика текстов
    # list_path_text = [textOriginal1, textOriginal2, textOriginal3]
    # thems_texts = ThemsText(list_path_text, trainTextUdpipe, optimal_topics=True)
    # view_srt, lda_model = thems_texts.view_thems()
    # list_thems_doc = thems_texts.topics_document(lda_model)
    # print(view_srt)
    # print()
    # for i in list_thems_doc:
    #     pprint(i)
    # pprint(list_thems_doc)

    # Морфологический анализ
    # morhp_an = TextAnalysis()
    # tokenPosList = morhp_an.morph_analysis(trainTextNLTK4russian, textOriginal1, rusTag=True)
    # pprint(tokenPosList)
    # print()
    # Синтаксическое дерево
    # view_tree = morhp_an.view_syntax_tree(textOriginal1, trainTextUdpipe)
    # print(view_tree)

    print("!!!!")



if __name__ == '__main__':
    main()
