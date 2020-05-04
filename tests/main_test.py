import nltk
from spacy import displacy

from parsing.metric.CosineSimilarity import CosineSimilarity
from parsing.metric.MetricAnalysis import MetricAnalysis
from parsing.metric.MetricJaccard import MetricJaccard
from parsing.metric.StohasticAnalysis import StohasticAnalysis
from parsing.text import Text
from parsing.semantic.Models import Models
from parsing.text_metric_analysis import text_metric_analysis

from parsing.text_analysis import text_analysis
import spacy_udpipe

trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


def main():
    # nltk.download('punkt')
    # nltk.download('stopwords')

    textOriginalList = [textOriginal3, textOriginal2]
    # Преобразовать в объекты Text
    # textsList = []
    # for textOriginal in textOriginalList:
    #     textsList.append(Text(textOriginal, trainTextUdpipe))
    # text_standart = Text(textOriginal1, trainTextUdpipe)


    j = StohasticAnalysis(trainTextUdpipe)
    j.set_text(textOriginal3)
    j.set_text_standart(textOriginal1)
    j.run()
    print(j.get_text().p)
    j.set_text(textOriginal2)
    j.run()
    print(j.get_text().p)

    # analysis = text_metric_analysis()
    # for text in textsList:
    #     # analysis.stochastic_analysis(text_standart, text)
    #     # analysis.distance_metrics_Jaccard(text_standart, text)
    #     analysis.cosine_similarity(text_standart, text)

    # text_new = Text(textOriginal2)
    # analysis1 = text_metric_teanalysis(trainTextUdpipe, text_standart, text_new=text_new)
    # print(analysis1.calculat_I(text_standart, text_new))
    print("!!!!")



if __name__ == '__main__':
    main()
