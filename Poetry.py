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

class Poetry_finder():
    def __init__(self, inputfile = "test.txt"):
        self.inputfile = inputfile
        self.queue = Queue()
        self.lines = []
        self.line_no_punct = []
        self.words = []

    def prepare(self):
        """This function will find a haiku based on an input file"""
        self.sentence_finder()
        self.strip_punctuation()
        self.split_words()

    def findHaiku(self):
        state = 0
        for sentence in self.words:
            syls = self.syllable_count(sentence)
            if (state ==  0) and  (syls == 5):
                self.queue.enqueue(sentence)
                state = 1
            elif (state == 1) and (syls == 7):
                self.queue.enqueue(sentence)
                state = 2
            elif (state == 2) and (syls == 5):
                self.queue.enqueue(sentence)
                state = 3
            if state == 3:
                self.queue.enqueue("------------")
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
            count += nysl(words)[0]
        return count
    def split_words(self):
        for sentences in self.line_no_punct:
            self.words.append(sentences[0].split())
def main():
    sentences = Poetry_finder("hhgttg.txt")
    #sentences.sentence_finder()
    #print(sentences.lines)
    #striped = sentences.strip_punctuation()
    #sentences.split_words()
    #d = sentences.words
    #k = sentences.syllable_count(d[0])
    sentences.prepare()
    sentences.findHaiku()

    #print (k)
    #print(striped)
    #d = cmudict.dict()
    #sentence = "denote"
    #def nsyl(word):
    #    for x in d[word.lower()]
    #        return len(list(y for y in x if isdigit(y[-1])))
    #print(nsyl(sentence))

main()
