# Poetry_Maker
Design
======
Objective make haikus, acrostic, cinquain, echo verse:
explore the nltk library
steps
-----

haiku
-----
* get a file as an input
* seperate the file by sentences (using nltk)
* traverse the list by length of syllables.
  perhaps we can sort the sentences by number of syllables if we don't care about the order.
* find sentences that have 5 syllables store in a queue
* find 7 syllables store in queue
* when three are found then deque into list
* return all the haikus found

acrostic
--------
* have user enter input file
* have user enter word
* separate the file by sentences
* traverse the list and compare the first letter.
* store into a queue
* return all acrostic poems

cinquain
--------
* find a line with two syllables
* find line with four syllables
* find line with 6 syllables
* find line with 8 syllables
* find line with 2 syllables
* return poem
