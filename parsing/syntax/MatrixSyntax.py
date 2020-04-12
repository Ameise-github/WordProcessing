import random
from nltk.parse.pchart import PCFG


# https://habr.com/ru/post/342162/?amp%3Butm_medium=rss&amp%3Butm_campaign=interesting

class MatrixSyntax:

    def init_wfst(self, tokens, grammar):
        """

        :param tokens: лист токенов
        :param grammar: грамматика которая используется для
        :return:
        """
        numtokens = len(tokens)
        wfst = [[None for i in range(numtokens + 1)] for j in range(numtokens + 1)]
        for i in range(numtokens):
            productions = grammar.productions(rhs=tokens[i])
            wfst[i][i + 1] = productions[0].lhs()
        return wfst

    def display(self, wfst, tokens):
        print('\nWFST ' + ' '.join([("%-3d" % i) for i in range(1, len(wfst))]))
        for i in range(len(wfst) - 1):
            print("%d   " % i, end=''),
            for j in range(1, len(wfst)):
                print("%-4s" % (1 if wfst[i][j] else '.'), end=''),
                # print("%-4s" % wfst[i][j] , end=''),
            print()

    def complete_wfst(self, wfst, tokens, grammar: PCFG):
        index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
        numtokens = len(tokens)
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
