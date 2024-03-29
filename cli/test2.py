import math
import matplotlib.pyplot as pylab
import nltk
import string
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

stopset = set(stopwords.words('russian'))
stopset = stopset.union({'это', 'весь', 'свой', 'который'})
stopset_light = {'а', 'и', 'но', 'как', 'что', 'который',
                 'в', 'на', 'о', 'по', 'с', 'у', 'к', 'за', 'из', 'от', 'под',
                 'не', 'ни', 'да', 'бы', 'ли', 'же', 'как', 'так', 'то',
                 'я', 'мы', 'ты', 'вы', 'он', 'она', 'оно', 'они',
                 'мой', 'наш', 'твой', 'ваш', 'его', 'ее', 'их', 'свой',
                 'меня', 'нас', 'тебя', 'вас', 'себя',
                 'быть', 'весь', 'это', 'этот', 'тот', ''
                 }

ru_POS = {'NOUN': 'Cуществительные', 'INFN': 'Глаголы (инфинитивы)', 'ADJF': 'Прилагательные',
          'ADVB': 'Наречия', 'NUMR': 'Числительные', 'NPRO': 'Местоимения', 'PREP': 'Предлоги',
          'CONJ': 'Союзы', 'PRCL': 'Частицы', 'INTJ': 'Междометия',
          'ADJS': 'Краткие прилагательные', 'COMP': 'Компаративы', 'VERB': 'Глаголы (личная форма)',
          'PRTF': 'Причастия', 'PRTS': 'Краткие причастия', 'GRND': 'Деепричастия',
          'PRED': 'Предикативы', None: 'Неопределено'}


def make_russian_plots():
    '''изменить шрифт на русский'''
    import matplotlib
    matplotlib.rcParams['font.family'] = 'Verdana'
    return


### ---работать со словами--- ###

def word_tokenize(text):
    '''текстовое слово токенизатор'''
    # слово токенизация
    words = nltk.word_tokenize(text)

    # удалить пунктуацию
    punctuation = string.punctuation + '–' + '—' + '…' + '...' + '..'
    words = [w for w in words if (w not in punctuation)]
    words = [w for w in words if not w.isdigit()]

    # чистящие слова
    words = [w.replace('\'', '').replace('`', '') for w in words]
    words = [w.replace('«', '').replace('»', '') for w in words]
    words = [w.replace('„', '').replace('“', '') for w in words]
    words = [w.replace('…', '') for w in words]
    words = [w.replace('—', '') for w in words]
    words = [w.replace('\ufeff', '') for w in words]

    # сделать буквы маленькими
    words = [w.lower() for w in words if w != '']

    # сделать текст NLTK
    text = nltk.text.Text(words)

    return text


def sent_tokenize(text):
    '''текстовое предложение токенизатор'''
    # токенизация предложения
    sent = nltk.sent_tokenize(text, language='russian')
    return sent


def  normalize(words):
    '''делает морфологический анализ'''
    parses = [morph.parse(w)[0] for w in words]
    #    words = [p.normal_form for p in parses if p.tag.POS != None]
    words = [p.normal_form for p in parses]
    POS = nltk.FreqDist([p.tag.POS for p in parses if p.tag.POS != None])
    return nltk.Text(words), POS


### ---работа с текстами--- ###

def filter_stops(word):
    '''фильтр для набора стоп-слов'''
    return word in stopset


def filter_stops_light(word):
    '''фильтр для световых стоп-слов'''
    return word in stopset_light


def apply_filter(words, filter_to_use):
    '''фильтрует текст с помощью filter_to_use'''
    return nltk.Text([w for w in words if not filter_to_use(w)])


def lexical_diversity(words):
    '''лексическое разнообразие'''
    vocab = words.vocab()
    return len(vocab) / len(words)


def find_bigrams(words, n, freq=10):
    ''''найди самые популярные биграммы'''
    bcf = BigramCollocationFinder.from_words(words)
    bcf.apply_freq_filter(freq)
    return bcf.nbest(BigramAssocMeasures.likelihood_ratio, n)


def find_trigrams(words, n, freq=10):
    ''''найти самые популярные триграммы'''
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(freq)
    return tcf.nbest(TrigramAssocMeasures.likelihood_ratio, n)


def words_length(words):
    '''распределение частот по токену'''
    return nltk.FreqDist([len(w) for w in words])


def word_with_length(words, length):
    '''находит токен с длиной, равной длине'''
    return [w for w in words if len(w) == length]


def sents_length(sents):
    '''распределение частот по токену'''
    return nltk.FreqDist([len(word_tokenize(s)) for s in sents])


def sent_with_length(sents, length):
    '''находит токен с длиной, равной длине'''
    return [s for s in sents if len(word_tokenize(s)) == length]


def get_POS(words):
    '''часть речевой статистики'''
    POS = nltk.FreqDist([morph.parse(w)[0].tag.POS for w in words])
    return POS


### ---выход--- ###

def Zipf(x, L, l):
    '''Закон Ципфа нормализуется по длине текста
        L - длина текста
        l - длина словарного запаса
    '''
    A = L / math.log(l)
    p = -1
    return A * x ** p


def plot_Zipf(words, start=1, end=25):
    '''сюжет закон Ципфа'''
    vocab = words.vocab()
    mc = vocab.most_common(end + 1)
    L = len(words)
    l = len(vocab)

    numbers = [x for x in range(start, end + 1)]
    counts_Zipf = [Zipf(x, L, l) for x in range(start, end + 1)]
    counts = [w[1] for w in mc[start:]]

    pylab.grid(True, color='silver')
    pylab.plot(numbers, counts_Zipf, color='k')
    pylab.plot(numbers, counts, linewidth=2)
    pylab.title("Word Frequency Distribution")
    pylab.xlabel("Words' Number")
    pylab.ylabel("Counts")
    pylab.show()
    #    vocab.plot(n)
    return


def plot_most_common(words, n):
    '''график дисперсии для n наиболее распространенных слов'''
    vocab = words.vocab()
    fd = vocab.most_common(n)
    vocab_most_common = [i[0] for i in fd]
    print(vocab_most_common)
    words.dispersion_plot(vocab_most_common)
    return


def plot_words_length(words):
    '''длина сюжета'''
    wl = words_length(words)
    lengths = sorted([i for i in wl])
    freqs = [wl.freq(i) for i in wl]

    #    pyplot.figure(figsize=(10,6))
    pylab.grid(True, color='silver')
    pylab.plot(lengths, freqs, linewidth=2)
    pylab.title("Word Length Frequency")
    pylab.xlabel("Word Length")
    pylab.ylabel("Frequency")
    pylab.show()

    mean = sum([lengths[i] * freqs[i] for i in range(len(wl))])
    print("Most popular length = {0}".format(wl.most_common()[0][0]))
    print("Mean length         = {0:.2f}".format(mean))
    return


def plot_sents_length(sents):
    '''длина сюжетных предложений'''
    sl = sents_length(sents)
    lengths = sorted([i for i in sl])
    freqs = [sl.freq(i) for i in sl]

    #    pyplot.figure(figsize=(10,6))
    pylab.grid(True, color='silver')
    pylab.plot(lengths, freqs, linewidth=2)
    pylab.title("Sentence Length Frequency")
    pylab.xlabel("Sentence Length")
    pylab.ylabel("Frequency")
    pylab.show()

    mean = sum([lengths[i] * freqs[i] for i in range(len(sl))])
    print("Most popular length = {0}".format(sl.most_common()[0][0]))
    print("Mean length         = {0:.2f}".format(mean))
    return


def plot_sents(sents, short, long):
    '''сюжет короткие и длинные предложения'''

    lengths = ['<=' + str(short), '>=' + str(long)]
    points = [(x, 0) for x in range(len(sents))
              if len(word_tokenize(sents[x])) <= short]

    points += [(x, 1) for x in range(len(sents))
               if len(word_tokenize(sents[x])) >= long]
    if points:
        x, y = list(zip(*points))
    else:
        x = y = ()
    pylab.plot(x, y, "b|", scalex=.1)
    pylab.yticks(list(range(len(lengths))), lengths, color="b")
    pylab.ylim(-1, len(lengths))
    #    pylab.title(title)
    pylab.xlabel("Sentence Offset")
    pylab.show()
    return


def print_POS(POS):
    '''распечатать часть речевой статистики'''
    S = sum([POS[i] for i in POS])
    POS_sorted = POS.most_common()

    for part in POS_sorted:
        print("{0:<25} {1:.2%}".format(ru_POS[part[0]], part[1] / S))
    return


## ---io--- ###

def read_file(file):
    '''читать текстовый файл'''
    #    print(file)
    try:
        f = open(file, 'r',encoding='utf-8')
        text = f.read()
    except:
        f = open(file, encoding='utf-8')
        text = f.read()
    f.close()
    return text


###### ---использование--- ######

def analyze(file):
    '''использование анализировать текстовый файл'''
    # считать файл
    text = read_file(file)
    # токенизация предложения
    sents = sent_tokenize(text)
    # слово токенизация
    words = word_tokenize(text)
    #фильтр
    words_filter = apply_filter(words, filter_stops)
    #делает морфологический анализ
    words_norm, POS = normalize(words)
    # фильтр
    words_norm_filter = apply_filter(words_norm, filter_stops)
    # make_russian_plots()

    # статистика
    vocab = words_norm.vocab()
    hapaxes = vocab.hapaxes()
    L = len(words_norm)
    l = len(vocab)
    print('\n')
    print("Длина текста       = {0} words".format(L))
    print("Длина словаря      = {0} words".format(l))
    print("Лексическое разнообразие = {0:.1%}".format(l / L))
    print("Hapaxes           = {0:.1%}".format(len(hapaxes) / l))

    plot_sents_length(sents)
    plot_words_length(words_filter)

    # части речи
    POS.plot()
    print_POS(POS)

    # словосочетания
    #    print('\n')
    #    print("Bigrams: {0}\n".format(find_bigrams(words_filter, 10)))
    #    print("Trigrams: {0}\n".format(find_trigrams(words_filter, 10)))

    # Zipf's law
    plot_Zipf(words_norm)
    plot_most_common(words_norm_filter, 15)
    return words_norm_filter


# analyze("../../resource/data/Evgeniy_Onegin.txt")
file= "../resource/data/text1.txt"
# считать файл
text = read_file(file)
# токенизация предложения
sents = sent_tokenize(text)
# слово токенизация
words = word_tokenize(text)
#делает морфологический анализ
words_norm, POS = normalize(words)
v = normalize(words)
# фильтр
words_norm_filter = apply_filter(words_norm, filter_stops)
# фильтр
words_filter = apply_filter(words, filter_stops)
print("sents:  \t" + str(sents))
print("words:  \t" + str(words))
print("words_norm_filter: \t" + str(words_norm_filter))
print("words_filter: \t" + str(words_filter))
print("POS:  \t")
for p in v:
    # for w1 in w:
    #     print(w1)
    for p1 in p:
        print(p1)