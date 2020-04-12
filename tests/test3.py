import nltk
# nltk.download('universal_tagset')
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
import pymorphy2
from parsing.graphematic.GraphematicAnalysis import GraphematicAnalysis

# text: str = "В нашем классе учатся самые артистичные ученики и ученицы."
# nltk.download('treebank')

# text: str = "Солнце пригрело. Побежали ручьи. Прилетели грачи. Птицы выводят птенцов. Весело скачет по лесу заяц.Лисица вышла на охоту и чует" \
#             " добычу. Волчица вывела волчат на поляну. Медведица рычит у берлоги. Над цветами летают бабочки и пчелы. Все рады весне и т.д."
# слово токенизация
# text1: str = "Солнце пригрело. Побежали Солнце ручьи. Прилетели грачи. Птицы выводят птенцов. грачи птенцов птенцов."
# words = nltk.word_tokenize(text1.lower())
# tags = nltk.pos_tag(words, lang='rus')

# print(words)

# test = GraphematicAnalysis("../../resource/data/text2.txt")
# test.get_sentences("../../resource/data/test_output.txt")

# токенизация предложения
# sent = nltk.sent_tokenize(text, language='russian')
# print(sent)

# morphAnalyzer = pymorphy2.MorphAnalyzer()
# m = morphAnalyzer.parse('мама')
# print(m)
# for y in m:
#     print(y.tag.POS)
#     print(y.tag)

# for w in words:
#     p: list[str] = morphAnalyzer.parse(w)
#     print(p)

# p: list = morphAnalyzer.parse("В")
# p.extend(morphAnalyzer.parse("."))
# print(p)
# print()
# for i in p:
#     print(i.tag)
# print()

# for w, tag in tagsDict:
#     # tagStr: str = tag
#     tagStr = tag.replace(',', ' ')
#     tagList: list = tagStr.split(' ')
#     for mTag in p:
#         # mTagStr: str = str(mTag.tag)
#         mTagStr = str(mTag.tag).replace(',', ' ')
#         mTagList: list = mTagStr.split(' ')
#         if sorted(tagList) == sorted(mTagList):
#             print(f"{w} - {sorted(tagList)}")
#             print(sorted(mTagList))
#             # print(f"tag.POS = {mTag.tag.POS}; tag.case = {mTag.tag.case}; tag.gender = {mTag.tag.gender}; tag.number = {mTag.tag.number}; "
#             #       f"normal_form = {mTag.normal_form}; word = {mTag.word}")
#             # print(mTag)
#             print()

#Просмотр стоп-слов
tokens = nltk.corpus.stopwords.words('russian')
print(tokens)

#Частота слов в тексте
# print("FreqDist1")
# freq_dist_pos = nltk.FreqDist(words)
# print(freq_dist_pos.most_common())

# freq = nltk.FreqDist(words)
# for key,val in freq.items():
#     print (str(key) + ':' + str(val))