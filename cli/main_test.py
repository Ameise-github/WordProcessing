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

textBrain1 = "../resource/data/text_brain1.txt"
textBrain2 = "../resource/data/text_brain2.txt"
textBrain3 = "../resource/data/text_brain3.txt"
textBrain4 = "../resource/data/text_brain4.txt"

textOriginal7 = "../resource/data/text_python1.txt"
textOriginal8 = "../resource/data/text_python2.txt"
textOriginal9 = "../resource/data/text_language.txt"
textOriginal10 = "../resource/data/text_news.txt"



def main():
    # nltk.download('punkt')
    # nltk.download('stopwords')

    # s = StochasticAlgorithm()
    # res = s.process(trainTextUdpipe, textOriginal7, textOriginal8)
    # res1 = s.process(trainTextUdpipe, textOriginal7, textOriginal9)
    # print("StochasticAlgorithm:  " + str(res) + "; " + str(res1))

    # c = CosineSimilarityAlgorithm()
    # res2 = c.process(trainTextUdpipe, textOriginal7, textOriginal8)
    # res3 = c.process(trainTextUdpipe, textOriginal7, textOriginal9)
    # print("CosineSimilarityAlgorithm:  " + str(res2) + "; " + str(res3))

    # j = JaccardAlgorithm()
    # res4 = j.process(trainTextUdpipe, textOriginal7, textOriginal2)
    # res5 = j.process(trainTextUdpipe, textOriginal7, textOriginal3)
    # print("JaccardAlgorithm:  " + str(res4) + "; " + str(res5))

    # Изменения одного текста
    PragmaticAdequacy = PragmaticAdequacyAlgorithm()
    I1 = PragmaticAdequacy.process(trainTextUdpipe, textBrain1, textBrain2)
    print("text Brain 1-2: " + str(I1))
    I2 = PragmaticAdequacy.process(trainTextUdpipe, textBrain2, textBrain3)
    print("text Brain 2-3: " + str(I2))
    I3 = PragmaticAdequacy.process(trainTextUdpipe, textBrain3, textBrain4)
    print("text Brain 3-4: " + str(I3))
    # I4 = PragmaticAdequacy.process(trainTextUdpipe, textOriginal6, textOriginal4)
    # print("text 6-4: " + str(I4))

    I5 = PragmaticAdequacy.process(trainTextUdpipe, textBrain2, textBrain1)
    print("text Brain 2-1: " + str(I5))
    I6 = PragmaticAdequacy.process(trainTextUdpipe, textBrain3, textBrain2)
    print("text Brain 3-2: " + str(I6))
    I7 = PragmaticAdequacy.process(trainTextUdpipe, textBrain4, textBrain3)
    print("text Brain 4-3: " + str(I7))


    # Тематика текстов
    # list_path_text = [textOriginal6, textOriginal7, textOriginal8, textOriginal9, textOriginal10]
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
