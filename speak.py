import os
import datetime

def tts(text):
    return os.system("espeak  -s 155 -a 200 "+text+" " )

tts("'This is a sentence'")
print("I am still going")
