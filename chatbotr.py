import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import scipy
import pandas
import tflearn
import tensorflow as tf
import random
import json
import speech_recognition as sr

# restore all of our data structures

import pickle

data = pickle.load( open( "training_data", "rb" ) )

words = data['words']

classes = data['classes']

train_x = data['train_x']

train_y = data['train_y']



# import our chat-bot intents file

import json

with open('intents.json') as json_data:

    intents = json.load(json_data)

# load our saved model

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


def clean_up_sentence(sentence):

    # tokenize the pattern

    sentence_words = nltk.word_tokenize(sentence)

    # stem each word

    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]

    return sentence_words



# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=False):

    # tokenize the pattern

    sentence_words = clean_up_sentence(sentence)

    # bag of words

    bag = [0]*len(words)  

    for s in sentence_words:

        for i,w in enumerate(words):

            if w == s: 

                bag[i] = 1

                if show_details:

                    print ("found in bag: %s" % w)



    return(np.array(bag))


model.load('./model.tflearn')

context = {}
ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return (random.choice(i['responses']))

            results.pop(0)

print("Start chatting with our chatbot")
ch = int(input("Choose 1.Text 2.Speech"))
if(ch == 1):    
    print("Hello")
    while(True):
        p = input("you : ")
        print("Bot : "+response(p))

if(ch == 2):
    while(True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Ask question our chatbot!")
            audio = r.listen(source)
         
        # Speech recognition using Google Speech Recognition
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            print("You said: " + r.recognize_google(audio))
            print("bot:"+(response(r.recognize_google(audio))))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))




