import wikipedia
import pyttsx3
import os
def wiki():
    a=input('search:')
    talk=pyttsx3.init()
    b = wikipedia.summary(a)
    print(b)

    talk.say(b)

    talk.runAndWait()

def shutdown():
    os.system(' shutdown /s /t 1')



