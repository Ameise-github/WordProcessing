from pprint import pprint

import nltk
from spacy import displacy

from parsing.ThemsText import ThemsText
from parsing.metric.CosineSimilarity import CosineSimilarity
from parsing.metric.MetricAnalysis import MetricAnalysis
from parsing.metric.MetricJaccard import MetricJaccard
from parsing.metric.PragmaticAdequacy import PragmaticAdequacy
from parsing.metric.StohasticAnalysis import StohasticAnalysis
from parsing.text import Text
from parsing.semantic.Models import Models
from parsing.text_metric_analysis import text_metric_analysis

from parsing.text_analysis import text_analysis
import spacy_udpipe

trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
trainTextNLTK4russian = '../resource/data/trainText.tab'
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


def main():
    # nltk.download('punkt')
    # nltk.download('stopwords')

    # j = StohasticAnalysis()
    # j.set_trainTextUdpipe(trainTextUdpipe)
    # j.set_text(textOriginal3)
    # j.set_text_standart(textOriginal1)
    # j.run()
    # print(j.get_text().p)
    # j.set_text(textOriginal2)
    # j.run()
    # print(j.get_text().p)

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
    # print(list_thems_doc)

    # Морфологический анализ
    morhp_an = text_analysis()
    tokenPosList = morhp_an.morph_analysis(trainTextNLTK4russian, textOriginal1)
    pprint(tokenPosList)
    print()
    # Синтаксическое дерево
    view_tree = morhp_an.view_syntax_tree(textOriginal1, trainTextUdpipe)
    print(view_tree)

    print("!!!!")



if __name__ == '__main__':
    main()
