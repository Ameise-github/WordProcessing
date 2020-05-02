import nltk
from parsing.text import Text
from parsing.semantic.Models import Models
from parsing.text_metric_analysis import text_metric_analysis

trainTextUdpipe = "../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe"
textOriginal1 = "../resource/data/text1.txt"
textOriginal2 = "../resource/data/text3.txt"
textOriginal3 = "../resource/data/text2.txt"
textOriginal4 = "../resource/data/Evgeniy_Onegin.txt"


def main():
    nltk.download('punkt')
    nltk.download('stopwords')

    textOriginalList = [textOriginal3, textOriginal2]
    models = Models()
    # Преобразовать в объекты Text
    textsList = []
    for textOriginal in textOriginalList:
        textsList.append(Text(textOriginal))
    text_standart = Text(textOriginal1)

    # analysis = text_metric_analysis(trainTextUdpipe, text_standart, textsList=textsList)
    # analysis.stochastic_analysis(text_standart, textsList)
    # analysis.distance_metrics_Jaccard(text_standart, textsList, models)
    # analysis.cosine_similarity(text_standart, textsList, models)

    text_new = Text(textOriginal2)
    analysis1 = text_metric_analysis(trainTextUdpipe, text_standart, text_new=text_new)
    print(analysis1.calculat_I(text_standart, text_new))


if __name__ == '__main__':
    main()
