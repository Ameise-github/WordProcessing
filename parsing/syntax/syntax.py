# Программа использует морфологические данные разбора PyMorphy2 и синтаксические правила АОТ для автоматического синтаксического разобра текста на русском языки в NLTK.
# Python 3, NLTK, pymorphy2
# -*- coding: utf-8 -*-
import codecs


class SyntaxAnalysis:
    def __init__(self, pathToFile):
        # загружаем PyMorphy2
        # self.m = pm.MorphAnalyzer()
        # открываем (создаем)файл с грамматикой, куда будут записываться правила
        # self.f = codecs.open("../resource/book_grammars/grammarRU.fcfg", mode="w", encoding="utf-8")
        self.pathToFile = pathToFile
        self.regulationsInFile(self.pathToFile)

    def regulationsInFile(self, pathToFile):
        '''
        записываем правила, которые вручную делаем (некоторые на основе правил из АОТ)
        :param pathToFile: файл в который надо писать правила
        :return:None
        '''
        f = codecs.open(pathToFile, mode="w", encoding="utf-8")
        f.writelines("% start XP\n")
        f.writelines("XP -> NP\n")
        f.writelines("XP -> VP\n")
        f.writelines("XP -> AdjP\n")
        f.writelines("XP -> AdvP\n")
        f.writelines("XP -> COMP\n")
        f.writelines("XP -> PP\n")
        f.writelines("XP -> NUMRNP\n")
        f.writelines("XP -> NUMR\n")
        f.writelines("XP -> S\n")
        f.writelines("XP -> CONJP\n")
        f.writelines("XP -> PREDP\n")
        f.writelines("XP -> PrtfP\n")

        f.writelines("S[-inv] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=0, G=?g]\n")
        f.writelines("S[-inv] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=?p, G=0]\n")
        f.writelines("S[-inv] -> AdjP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=0, G=?g]\n")
        f.writelines("S[-inv] -> AdjP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=?p, G=0]\n")
        # f.writelines("S[-inv, +1] -> NP[C=nomn, NUM=plur, PER=?p] VP[NUM=?n, PER=0, G=None]\n")
        f.writelines("S[+adj] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] AdjP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
        f.writelines("S[-inv] -> NUMRNP[C=nomn] VP\n")
        f.writelines("S[+inv] -> VP[NUM=?n, PER=0, G=?g] NP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
        f.writelines("S[+inv] -> VP[NUM=?n, PER=?p, G=0] NP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
        f.writelines("S[+advp] -> AdvP S[+advp]\n")
        f.writelines("S[+advp] -> NP[C=gent, NUM=?n, PER=?p, G=?g] AdvP\n")
        # f.writelines("S[+infn] -> VP[+infn] VP\n")
        f.writelines("S[+predp] -> NP[C=datv] PREDP\n")
        f.writelines("S[+comp] -> NP[C=datv] COMP\n")

        f.writelines("S -> CONJ S\n")
        f.writelines("S -> NP[C=nomn, NUM=?n] '-' NP[C=nomn, NUM=?n]\n")
        f.writelines("S[+S] -> S ',' CONJ S\n")
        f.writelines("S[+S] -> S ',' S\n")
        f.writelines("S[+S] -> S ',' VP\n")

        # f.writelines("S[+advp] -> NP[C=datv, NUM=?n, PER=?p, G=?g] VP[+advp]\n")

        f.writelines("PREDP -> PREDP  VP[TR=?tr, NUM=0, PER=0, G=0]\n")
        f.writelines("PREDP -> AdvP PREDP\n")
        f.writelines("PREDP -> PRED\n")

        f.writelines("NUMRNP[C=?c] -> NUMR[C=?c] NP[C=?c, NUM=plur]\n")  # числительные в неименительном
        f.writelines("NUMRNP[C=accs] -> NUMR[C=accs] NP[C=gent]\n")  # числительные в винительном
        f.writelines("NUMRNP[+nomn, C=nomn] -> NUMR[C=nomn] NP[C=gent]\n")
        f.writelines("NUMR[C=?c] -> NUMR[C=?c] NUMR[C=?c]\n")  # ????

        f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=datv, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=loct, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=accs, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=gent, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=ablt, G=?g, NUM=?n, PER=?p]\n")  # предлог + ИГ (ПГ)
        f.writelines("PP -> PREP NUMRNP[-nomn]\n")  # предлог + гуппа числ
        f.writelines("PP[+advb] -> AdvP PP\n")
        f.writelines("PP -> PP AdvP\n")

        f.writelines("AdvP[+conj] -> AdvP CONJ AdvP\n")  # ОДНОР_НАР
        f.writelines("AdvP[+numr] -> AdvP NUMRNP\n")
        # f.writelines("AdvP -> ADVB ADVB\n")
        f.writelines("AdvP -> ADVB AdvP\n")
        f.writelines("AdvP -> ADVB\n")
        f.writelines("PrtfP[C=?c, G=?g, NUM=?n] -> PRTF[C=?c, G=?g, NUM=?n]\n")
        f.writelines("PrtfP[+pp, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] PP\n")
        f.writelines("PrtfP[+instr, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] NP[C=ablt]\n")
        f.writelines("PrtfP[+instr, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] AdvP\n")

        f.writelines(
            "NP[+adjf, C=?c, G=?g, NUM=sing] -> AdjP[C=?c, G=?g, NUM=sing] NP[C=?c, G=?g, NUM=sing]\n")  # именная группа (ПРИЛ-СУЩ)
        f.writelines(
            "NP[+adjf, C=?c, NUM=plur] -> AdjP[C=?c, NUM=plur] NP[C=?c, NUM=plur]\n")  # именная группа мн.ч. (ПРИЛ-СУЩ)
        f.writelines("NP[+gent, C=?c, G=?g, NUM=?n] -> NP[C=?c, G=?g, NUM=?n] NP[C=gent]\n")  # ГЕНИТ_ИГ
        f.writelines(
            "NP[+prtf, C=?c, G=?g, NUM=sing] -> PrtfP[C=?c, G=?g, NUM=sing] NP[C=?c, G=?g, NUM=sing]\n")  # именная группа (ПРИЛ-СУЩ)
        f.writelines(
            "NP[+prtf, C=?c, NUM=plur] -> PrtfP[C=?c, NUM=plur] NP[C=?c, NUM=plur]\n")  # именная группа мн.ч. (ПРИЛ-СУЩ)
        f.writelines("NP[C=?c, +conj] -> NP[C=?c] CONJ NP[C=?c]\n")
        f.writelines("NP[C=?c, G=?g, NUM=?n, PER=?p] -> NOUN[C=?c, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("NP[C=?c, NUM=?n, PER=?p, G=?g] -> NPRO[C=?c, NUM=?n, PER=?p, G=?g]\n")
        f.writelines("NP[+pp, C=?c, G=?g, NUM=?n] -> NP[C=?c, G=?g, NUM=?n] PP\n")
        f.writelines("NP[+prcl, C=?c, G=?g, NUM=?n] ->PRCL NP[C=?c, G=?g, NUM=?n]\n")

        f.writelines("NP[+particip, C=?c, NUM=plur] -> NP[C=?c, NUM=?n] ',' PrtfP[C=?c, NUM=?n] \n")

        f.writelines(
            "VP[+advb, TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> AdvP VP[TENSE=?t, TR=?tr, G=?g, NUM=?n, PER=?p]\n")  # наречие + глагол (НАРЕЧ_ГЛАГОЛ)
        f.writelines("VP[+advb, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] AdvP\n")
        f.writelines(
            "VP[+infn, TR=?tr, NUM=?n, PER=?p, G=?g] -> VP[NUM=?n, PER=?p, G=?g] VP[TR=?tr, NUM=0, PER=0, G=0]\n")  # ГГ + инфинитив (ПЕР_ГЛАГ_ИНФ)
        f.writelines(
            "VP[+objt, NUM=?n, PER=?p, G=?g] -> VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran] NP[C=accs]\n")  # глагол + прямое дополнение (ПРЯМ_ДОП)
        f.writelines(
            "VP[+objt, NUM=?n, PER=?p, G=?g] -> VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran] NP[C=gent]\n")  # глагол + прямое дополнение в генетиве(ПРЯМ_ДОП)
        f.writelines(
            "VP[+objt, NUM=?n, PER=?p, G=?g, TR=tran] -> NP[C=accs] VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran]\n")  # глагол + прямое дополнение (ПРЯМ_ДОП)
        f.writelines(
            "VP[TENSE=?t, G=?g, NUM=?n, PER=?p, TR=?tr] -> INFN[TENSE=?t, G=?g, NUM=?n, PER=?p, TR=?tr]\n")  # CHTO ETO??
        f.writelines("VP[+instr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NP[C=ablt]\n")
        f.writelines("VP[+pp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] PP\n")
        f.writelines("VP[+pp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> PP VP[TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("VP[+datv, TENSE=?t, G=?g, NUM=?n, PER=?p] ->VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NP[C=datv]\n")
        f.writelines("VP[+adj, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] AdjP[С=ablt]\n")
        f.writelines("VP[+comp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] COMP\n")
        f.writelines("VP[+numr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NUMRNP\n")
        f.writelines("VP[+neg, TENSE=?t, G=?g, NUM=?n, PER=?p] -> 'не' VP[TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
        f.writelines("VP[TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VERB[TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
        # f.writelines("VP[+infn] -> VP VP[+infn]\n")

        f.writelines(
            "AdjP[+advb, C=?c, G=?g, NUM=?n] -> AdvP AdjP[C=?c, G=?g, NUM=?n]\n")  # наречие + прилагательное (НАР_ПРИЛ)
        f.writelines("AdjP[+advb, C=?c, G=?g, NUM=?n] -> AdjP[C=?c, G=?g, NUM=?n] PP\n")
        f.writelines(
            "AdjP[C=?c, G=?g, NUM=?n, +conj] -> AdjP[C=?c, G=?g, NUM=?n] CONJ AdjP[C=?c, G=?g, NUM=?n]\n")  # ОДНОР_ПРИЛ
        f.writelines("AdjP[C=?c, G=?g, NUM=?n] -> ADJF[C=?c, G=?g, NUM=?n]\n")
        f.writelines("AdjP[+adjs, G=?g, NUM=?n] -> ADJS[G=?g, NUM=?n]\n")

        f.writelines("COMP[+conj] -> COMP CONJ COMP\n")
        f.writelines("COMP[+advb] -> AdvP COMP\n")
        f.writelines("COMP[+noun, +comp] -> COMP[-comp] NP[C=gent]\n")
        f.writelines("COMP[+vp] -> COMP VP\n")

        f.writelines("INFN[+conj] -> INFN CONJ INFN\n\n\n")  # ОДНОР_ИНФ

        f.writelines("CONJP[+vp] -> CONJ VP\n\n\n")

        f.close()


    def pm2fcfg(self,tagsDict, pathToFile, morphAnalyz):
        """
        функция, которая переводит нужную нам информацию из пайморфи в вид, читаемый парсером NLTK
        принимает (токенизированное) словосочетание на входе, записывает правила (lexical productions) в тот же файл с грамматикой

        :param phrase: (токенизированное) словосочетание для разбора (или текст)
        :type phrase: []
        :param tagsDict: список слов и теггов
        :type tagsDict: list
        :param pathToFile: файл граматики для записи
        :type pathToFile: File
        :param morphAnalyz: объект морфологического анализатора
        :type morphAnalyz: MorphAnalyzer()
        """
        tokenPos = []
        f = codecs.open(pathToFile, mode="a", encoding="utf-8")
        for word, tag in tagsDict:
            tStr = tag.replace(',', ' ')
            tList = tStr.split(' ')
            flag = False
            # a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
            # от части речи зависит, какие признаки отправляются в грамматику, отсюда условия
            a = morphAnalyz.parse(word)
            for y in a: # y - объект, а - лист
                y_word = str(y.word).replace('ё', 'е')
                y_normal_form = str(y.normal_form).replace('ё', 'е')

                yStr = str(y.tag).replace(',', ' ')
                yTagList = yStr.split(' ')
                if sorted(tList) == sorted(yTagList):
                    strk = ""
                    tagPos = y.tag.POS
                    if (tagPos == "NOUN") or (tagPos == "ADJF") or (tagPos == "PRTF"):
                        strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(
                            y.tag.number) + ", PER=3" + ", NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    elif (tagPos == "ADJS") or (tagPos == "PRTS"):
                        strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", NF=u'" + str(
                            y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    elif (tagPos == "NUMR"):
                        strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF=u'" + str(y_normal_form) + "'] -> '" + str(
                            y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    elif (tagPos == "ADVB") or (tagPos == "GRND") or (tagPos == "COMP") or (tagPos == "PRED") or (
                            tagPos == "PRCL") or (tagPos == "INTJ"):
                        strk = str(y.tag.POS) + "[NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    elif (tagPos == "PREP") or (tagPos == "CONJ"):
                        strk = str(y.tag.POS) + "[NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                        # break
                    elif (tagPos == "NPRO") & (y_normal_form != "это") & (y_normal_form != "нечего"):
                        if ((y.tag.person[0] == "3") & (y.tag.number == "sing")):
                            strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(
                                y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(
                                y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        else:
                            strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NUM=" + str(y.tag.number) + ", PER=" + \
                                   str(y.tag.person)[0] + ", NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    elif (tagPos == "VERB") or (tagPos == "INFN"):
                        if (y.tag.tense == "past"):
                            strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(
                                y.tag.tense) + ", G=" + str(y.tag.gender) + ", NUM=" + str(
                                y.tag.number) + ", PER=" + "0" + ", NF=u'" + str(y_normal_form) + "'] -> '" + str(
                                y_word) + "'\n"
                        elif (y.tag.POS == "INFN"):
                            strk = str(y.tag.POS) + "[TR=" + str(
                                y.tag.transitivity) + ", TENSE=0, G=0, NUM=0, PER=0, NF=u'" + str(
                                y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        else:
                            strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(
                                y.tag.tense) + ", G=" + "0" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[
                                       0] + ", NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                        # f.writelines(strk)
                        flag = True
                    else:
                        yTag = str(y.tag)
                        if (yTag == "PUNCT"):
                            strk = str('NONLEX') + "[NF=u'" + str(y_normal_form) + "'] -> '" + str(y_word) + "'\n"
                            # f.writelines(strk)
                            flag = True
                            # break
                    if flag:
                        f.writelines(strk)
                        tokenPos.append(y)
                        break
        f.close()
        return tokenPos

# s:str = "В нашем классе учатся самые артистичные ученики и ученицы"
# сюда пишется словосочетание для разбора
# text = input("")
# разбиваем словосочетание на токены
# words = word_tokenize(s.lower(), language="russian")

# запускаем функцию, описанную выше
# pm2fcfg(words)
# построить синтаксический анализатор
# cp = load_parser('../resource/book_grammars/grammarRU.fcfg', trace=1)

# for tree in cp.parse(words):
#     print(tree)
