
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
import Poetry.py
from Poetry import Poetry_finder




def main():
    text = raw_input("What is the file you want to make poems from? Include .txt "  )
    sentences = Poetry_finder(text)
    sentences.prepare()
    
    choice = raw_input("Type 1 to make an Acrostic, 2 to make a haiku: " )
    
    
    if choice == 1:
        acrostic = raw_input("what word would you like to make the acrostic? ")
        sentences.findAcrostic(acrostic)
    
    else:
    
        sentences.findHaiku()
    
    
main() 