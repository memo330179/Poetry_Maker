import nltk
import nltk.data
from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
import pickle
from queue import Queue
import re
import curses
from curses.ascii import isdigit
import string
import urllib
from bs4 import BeautifulSoup

class Poetry_finder():
    def __init__(self, inputfile = "test.txt"):
        self.inputfile = inputfile
        self.queue = Queue()
        self.lines = []
        self.line_no_punct = []
        self.words = []
        self.tmpQueue = Queue()

    def prepare(self):
        """This function will find a haiku based on an input file"""
        self.sentence_finder()

    def findHaiku(self):
        state = 0
        for sentence in self.lines:
            syls = self.syllable_count_fail(sentence)
            if (state ==  0) and  (syls == 5):
                self.queue.enqueue(sentence)
                self.tmpQueue.enqueue(sentence)

                state = 1
            elif (state == 1) and (syls == 7):
                 self.tmpQueue.enqueue(sentence)
                 self.queue.enqueue(sentence)
                 state = 2
            elif (state == 2) and (syls == 5):
                self.queue.enqueue(sentence)
                self.tmpQueue.enqueue(sentence)
                state = 3
            if state == 3:
                self.queue.enqueue("------------")
                for i in range(self.tmpQueue.size()):
                    line = self.tmpQueue.dequeue()
                    print(line)
                print("--------")
                state = 0
        self.printHaiku()
    def printHaiku(self):
        for i in range(self.queue.size()):
            print (self.queue.dequeue())
    def sentence_finder(self):
        """This function will divide the input file into sentences and organize them"""
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        fp = open(self.inputfile)
        data = fp.read()

        self.lines= tokenizer.tokenize(data)

    def find_component(self, syl):
        """This function will find a sentence that contains the number of syllables needed puts them into queues divided up into haikus"""
        return 0
    def strip_punctuation(self):
        """strips the punctuation of a sentence so that python does not get confused"""
        sentence_list = []
        for sentences in self.lines:
            lower_case = str.lower(sentences)
            #sentence_list.append([lower_case.translate(str.maketrans("",""), string.punctuation)])
            sentence_list.append([re.sub("[\.\t\,\:;\(\)\.\!\?]", "", lower_case, 0, 0)])

        self.line_no_punct = sentence_list
    def syllable_count(self, sentence):
        """counts syllables in a sentence"""

        d = cmudict.dict()
        def nysl(word):
            return[len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
        count = 0
        for words in sentence:
            try:
                count += nysl(words)[0]
            except KeyError:
                count += self.syllable_count_fail(words)
        return count

    def syllable_count_fail(self, word):
        url = 'http://www.wordcalc.com/index.php'
        pala = {'text': word }
        post_data = urllib.parse.urlencode(pala)
        post_data = '%s&optionSyllableCount&optionWordCount' % post_data
        binary_data = post_data.encode('ascii')
        cnxn = urllib.request.urlopen(url, binary_data)
        response = cnxn.read()
        cnxn.close()

        soup = BeautifulSoup(response, "html.parser")
        h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics']
        if len(h3_matches) != 1:
              raise Exception('Wrong number of <h3>Statistics</h3>')
        h3_match = h3_matches[0]
        table = h3_match.findNextSibling('table')

        td_matches = [td for td in table.findAll('td')
                        if td.text == 'Syllable Count']
        if len(td_matches) != 1:
            raise Exception('Wrong number of <td>Syllable Count</td>')
        td_match = td_matches[0]

        td_value = td_match.findNextSibling('td')
        syllable_count = int(td_value.text)
        return syllable_count
    def split_words(self):
        for sentences in self.line_no_punct:
            self.words.append(sentences[0].split())

def main():
    sentences = Poetry_finder("Oedipus_Rex.txt")
    #sentences.sentence_finder()
    #print(sentences.lines)
    #striped = sentences.strip_punctuation()
    #sentences.split_words()
    #d = sentences.words
    #k = sentences.syllable_count(d[0])
    sentences.prepare()
    sentences.findHaiku()
    #count = sentences.syllable_count_fail("denote")
    #print(count)
    #print (k)
    #print(striped)
    #d = cmudict.dict()
    #sentence = "denote"
    #def nsyl(word):
    #    for x in d[word.lower()]
    #        return len(list(y for y in x if isdigit(y[-1])))
    #print(nsyl(sentence))

main()
