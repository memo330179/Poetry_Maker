
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
from Poetry import Poetry_finder




def main():
    text = input("What is the file you want to make poems from? Include .txt "  )
    sentences = Poetry_finder(text)
    sentences.prepare()

    choice = int(input("Type 1 to make an Acrostic, 2 to make a haiku: " ))


    if choice == 1:
        acrostic = input("what word would you like to make the acrostic? ")
        sentences.findAcrostic(acrostic)

    else:

        sentences.findHaiku()

    print("Would you like to see the poems again?")

    choice = str(input("Type yes to play again " ))

    if choice == "yes":
        sentences.printhaiku()




main()
