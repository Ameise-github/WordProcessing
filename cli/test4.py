# import nltk
# from nltk.parse.chart import demo_grammar

# EarleyChartParser

# The grammar for ChartParser and SteppingChartParser:
# grammar = demo_grammar()
#
# print("* Grammar")
# print(grammar)
# grammar = nltk.data.load('file:D:/Projects/ProjectPython/WordProcessing/resource/book_grammars/grammarRU.fcfg')
#попробовать
# print("* parse")
# sr_parse = nltk.ShiftReduceParser(grammar)
# sent = 'I saw John with a dog with my cookie'.split()
# tmp = sr_parse.parse(sent)
# for t in tmp:
#     print(t)

# tokens = "рос маленький  одинокий одуванчик".split()
# tokens = "I saw John with a dog with my cookie".split()

# Do the parsing.
# earley = nltk.EarleyChartParser(grammar, trace=1)
# t = perf_counter()
# chart = earley.chart_parse(tokens)
# parses = list(chart.parses(grammar.start()))
# t = perf_counter() - t

# Print results.
# if numparses:
# assert len(parses) == 5, "Not all parses found"
# if print_trees:
# for tree in parses:
    # print(tree)
    # tree.draw()
# else:
#     print("Nr trees:", len(parses))


#UDPipe + spaCy
from pprint import pprint

from spacy import displacy
from pathlib import Path
import spacy_udpipe
import numpy
from spacy.tokens import Doc
# download Russian model
# spacy_udpipe.download("ru")
# text = "соседнем дворе рос маленький одинокий одуванчик тянулся солнцу своими зелеными листьями листья напитаны зеленой жижей"
# nlp = spacy_udpipe.load("ru")

#Объект spaCy
# doc = nlp(text)
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.dep_)

#Загрузить пользовательскую модель
# print("\nС другой моделью  не по умолчанию (Получилось одинаково, попробовать другоую модель)")
# nlp1 = spacy_udpipe.load_from_path(lang="ru",
#                                   path="../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe",
#                                   meta={"description": "Custom 'ru' model"})
# doc1 = nlp1(text)
# for token1 in doc1:
#     print(token1.text, token1.lemma_, token1.pos_, token1.dep_)

#Построение дерева
#Строится дерево по 1-му предложению. Выводит код в html
# print("\nДерево")
# html = displacy.render(doc1, style="dep")
# print(html)

#Обход по дереву
# print("\nПроход по дереву:")
#dep_ - тип связи

# for token in doc1:
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#             [child for child in token.children])

# print("\nобъект span:")
#span - часть документа
# span = doc1[doc1[4].left_edge.i : doc1[4].right_edge.i+1]
# with doc1.retokenize() as retokenizer:
#     retokenizer.merge(span)
# for token in doc1:
#     print(token.text, token.pos_, token.dep_, token.head.text)

# print("\n\n Поправки")
# head - с чем связан
# n = len(doc1)
# matrix = numpy.zeros((n,n), dtype=float)
# for token in doc1:
#     for child in token.children:
#         matrix[token.i][child.i] = 1
#
# print("Matrix")
# for x in matrix:
#     print(x)
#
# print("\nChild token")
# for token in doc1:
#     for child in token.children:
#         print(token.i, token.text, [child.i, child])


#Рисование дерева зависимостей
from nltk.tree import Tree
from nltk.draw import TreeView


def nltk_spacy_tree(text):
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    nlp = spacy_udpipe.load_from_path(lang="ru",
                                       path="../resource/trainModel/russian-syntagrus-ud-2.5-191206.udpipe",
                                       meta={"description": "Custom 'ru' model"})
    doc = nlp(text)

    def token_format(token):
        # return "_".join([token.orth_, token.tag_, token.dep_])
        return "_".join([token.orth_, token.pos_])

    def to_nltk_tree(node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(token_format(node),
                        [to_nltk_tree(child)
                         for child in node.children]
                        )
            # return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
        else:
            return token_format(node)

    tree = [to_nltk_tree(sent.root) for sent in doc.sents]
    # Первый элемент в списке - полное дерево
    # tree[0].draw()
    # ttt = TreeView(tree[0])._cframe.print_to_file('output.ps')
    ttt = TreeView(tree[0])._cframe
    # вернуть путь
    print()

nltk_spacy_tree("В соседнем дворе рос маленький и одинокий одуванчик Он тянулся к солнцу своими зелеными листьями.")
