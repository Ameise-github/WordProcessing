# coding:utf8
import random

import nltk
from pathlib import Path


def init_wfst(tokens, grammar):
    numtokens = len(tokens)
    wfst = [[None for i in range(numtokens + 1)] for j in range(numtokens + 1)]
    for i in range(numtokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i + 1] = productions[0].lhs()
    return wfst


def display(wfst, tokens):
    print('\nWFST ' + ' '.join([("%-3d" % i) for i in range(1, len(wfst))]))
    for i in range(len(wfst) - 1):
        print("%d   " % i, end=''),
        for j in range(1, len(wfst)):
            print("%-4s" % (1 if wfst[i][j] else '.'), end=''),
            # print("%-4s" % wfst[i][j] , end=''),
        print()


def complete_wfst(wfst, tokens, grammar):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    old = -1
    for span in range(2, numtokens + 1):
        for start in range(numtokens + 1 - span):
            end = start + span
            for mid in range(start + 1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                vr = random.randint(0, 20)
                # if nt1 and nt2 and (nt2, nt1) in index:
                if vr == 1:
                    # wfst[start][end] = index[(nt1, nt2)]
                    wfst[start][end] = 1
                    # if trace:
                    #     print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" %
                    #           (start, nt1, mid, nt2, end, start, index[(nt1, nt2)], end))
    return wfst


# grammar = nltk.data.load('file:D:/Projects/ProjectPython/WordProcessing/resource/book_grammars/grammarRU.fcfg')
grammar_file= '/resource/book_grammars/grammarRU.fcfg'
cp = nltk.parse.load_parser('file:'+grammar_file, trace=1)
grammar = cp.grammar()
# ChartParser
tokens = "в соседнем дворе рос маленький  одинокий одуванчик он тянулся солнцу своими зелеными листьями его листья написаты зеленой жижей".split()
print("wfst0")
wfst0 = init_wfst(tokens, grammar)
display(wfst0, tokens)
print("\nwfst1")
wfst1 = complete_wfst(wfst0, tokens, grammar)
display(wfst1, tokens)

# for p in grammar.productions():
#     p.lhs()
#     print(p.)
# print(grammar.productions())

# v1 = grammar.productions(rhs=tokens[0])
# v2 = grammar.productions(rhs=tokens[2])
# print(v1)
# for vv in v1:
#     print(vv.rhs().type())
#     print(type(vv))
#     print(vv.is_lexical())
#     print("\n\tLEFT")
#     print(vv.rhs())
#     for vv2 in v2:
#         print("\n\tRIGHT V2")
#         print(vv2.lhs())
#         print("\n\tLEFT V2")
#         print(vv2.rhs())
# print(type(vv))

# v1 = grammar.is_lexical()
# print(v1)


#Синтаксическаие деревья
# Нарисовать синтаксическое дерево
# n = cp.parse(textTokenz)
# for obj in n:
#     print(obj)
#     d = obj.draw()
#
# grammar = nltk.data.load('file:D:/Projects/ProjectPython/WordProcessing/resource/book_grammars/grammarRU.fcfg')
# parser = parse.FeatureEarleyChartParser(grammar)
# trees = parser.parse(textTokenz)
# for tree in trees:
#     tree.draw()
    # print(tree.pformat_latex_qtree())
    # ptree = nltk.tree.ParentedTree.convert(tree)
    # print(ptree)



