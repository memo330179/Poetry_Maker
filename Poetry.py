#all of the imports
import nltk 
import nltk.data 
from nltk.corpus import wordnet as wn  
from nltk.corpus import cmudict
from queue import Queue
import re
import curses
from curses.ascii import isdigit
import string
import urllib
from bs4 import BeautifulSoup
import os

class Poetry_finder():
    def __init__(self, inputfile = "test"):
        """Inititalizer. This function initializes the class"""
        self.inputfile = inputfile # this is the input file the class will need
        self.queue = Queue() #this will store the result so that we won't need to do the calculations later
        self.lines = [] # we will store the sentences here
        self.line_no_punct = [] # this will store sentences without punctuation
        self.words = [] # this will store the words of the sentences
        self.tmpQueue = Queue() # a temporary queue for various uses
        self.acrostic_queue = Queue() # a queue that will store the acrostic poems found

    def prepare(self):
        """This function will prepare verything to make poetry"""
        self.sentence_finder() # calls sentence finder

    def findHaiku(self):
        state = 0 # state 0 means that we are looking for the first sentence
        for sentence in self.lines: # iterate through the sentences
            syls = self.syllable_count_fail(sentence) #syllables counted
            if (state ==  0) and  (syls == 5): # looking for 5 syllables 
                self.queue.enqueue(sentence) # enqueue the sentence 
                self.tmpQueue.enqueue(sentence) # temporarily enqueue the sentence

                state = 1 
            elif (state == 1) and (syls == 7): # looking for a seven syllable sentence if the first one has beem found
                 self.tmpQueue.enqueue(sentence)
                 self.queue.enqueue(sentence)
                 state = 2
            elif (state == 2) and (syls == 5): # looking for a five syllable sentence
                self.queue.enqueue(sentence)
                self.tmpQueue.enqueue(sentence)
                state = 3
            if state == 3: # a haiku has been found
                for i in range(self.tmpQueue.size()): # dequeue the temporary
                    line = self.tmpQueue.dequeue() 
                    print(line) #print for the viewer
                    #speak = self.speak("'"+line+"'") # uncommment to have linux read it
                print("--------") # print a pretty little divider
                self.queue.enqueue("------------") #add a pretty little divider
                state = 0 # start again
        #self.printHaiku()
    def findAcrostic(self, acrostic):
        index = 0 # start an index
        for sentence in self.lines: # irerate through the sentence
            try: # we will eventually reach an error
                lower = sentence[0].lower() # make sure the first letter is lowered
                if acrostic[index].lower() == lower: # if the acrostic word is the same as the first letter
                    self.tmpQueue.enqueue(sentence) # add to the queue
                    index += 1 # find next letter
            except IndexError: # we will reach the end of the word
                for i in range(self.tmpQueue.size()):
                    sentence = self.tmpQueue.dequeue()
                    print(sentence)
                    index = 0
    def printHaiku(self): # print the haiku
        for i in range(self.queue.size()):
            print (self.queue.dequeue())
    
    
    def sentence_finder(self):
        """This function will divide the input file into sentences and organize them"""
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') # load the tokenizer
        fp = open(self.inputfile) #open the file
        data = fp.read() 

        self.lines= tokenizer.tokenize(data) # divide into sentences


    def strip_punctuation(self):
        """strips the punctuation of a sentence so that python does not get confused"""
        sentence_list = []
        for sentences in self.lines:
            lower_case = str.lower(sentences)
            #sentence_list.append([lower_case.translate(str.maketrans("",""), string.punctuation)])
            sentence_list.append([re.sub("[\.\t\,\:;\(\)\.\!\?]", "", lower_case, 0, 0)])

        self.line_no_punct = sentence_list
    def syllable_count(self, sentence):
        """counts syllables in a sentence. This is no longer used"""

        d = cmudict.dict() #this is the dictionary with all the words on it
        def nysl(word): # finds the syllables
            return[len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
        count = 0
        for words in sentence:
            try:
                count += nysl(words)[0]
            except KeyError:
                count += self.syllable_count_fail(words)
        return count

    def syllable_count_fail(self, word):
        url = 'http://www.wordcalc.com/index.php' # this website counts syllables
        pala = {'text': word } # the input type is text we want to sent the sentence
        post_data = urllib.parse.urlencode(pala) # encode it so that the server can read it
        post_data = '%s&optionSyllableCount&optionWordCount' % post_data # make astring with the post we want
        binary_data = post_data.encode('ascii') # encode into ascii to iterate through
        connection = urllib.request.urlopen(url, binary_data) # this requests from the url with the post we sent
        response = connection.read() # we get a response back
        connection.close() # we close the connection

        soup = BeautifulSoup(response, "html.parser") #make a beautiful soup object
        h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics'] # find h3s with the value statistics
        if len(h3_matches) != 1: # this page has only one statistics page
              raise Exception('Wrong number of <h3>Statistics</h3>') #raise exception
        h3_match = h3_matches[0] #use the first match
        table = h3_match.findNextSibling('table') #find the table element

        td_matches = [td for td in table.findAll('td') #find all the tables that say syllable count
                        if td.text == 'Syllable Count']
        if len(td_matches) != 1: #this page only has one td with <td>Syllable Count</td>
            raise Exception('Wrong number of <td>Syllable Count</td>')
        td_match = td_matches[0] #use the first one

        td_value = td_match.findNextSibling('td') # find the sibling that to this
        syllable_count = int(td_value.text) # get the value of this td
        return syllable_count #return it
    def split_words(self):
        """Splits the sentence into words"""
        for sentences in self.line_no_punct:
            self.words.append(sentences[0].split())
    def speak(self, text):
        #speaks for linux
        return os.system("espeak  -s 155 -a 200 "+text+" " )
