import json
import os
import datetime
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from emoji_parse import EmojiDict

from wordcloud import WordCloud



fileDirectory = "wordClouds"
if not os.path.exists(fileDirectory):
    os.makedirs(fileDirectory)



stopwordFile = "data/stopwords_de.json"
with open(stopwordFile) as jsonContent:

    wordcloudStopWords = json.load(jsonContent)




chatChronologyFile = "chatlog.json"
with open(chatChronologyFile) as jsonContent:

    chatContent = json.load(jsonContent)

messages = chatContent["messages"]

users = {}
userTexts = {}

dates = {}
dates2 = []

# "date": "2016-01-09T10:26:04",

for message in messages:

    if message["type"] == "message":

        if message['from'] not in users.keys() and message['from'] not in userTexts.keys():
            users[message["from"]] = 0
            userTexts[message['from']] = [message["text"]]

        else:
            users[message["from"]] += 1
            userTexts[message["from"]].append(message["text"])








formatString = ""
for user in users.keys():

    userText = ""

    rawData = userTexts[user]

    for text in rawData:

        if not isinstance(text, (list,)):
            userText += " " + text.lower()


    print(user)


    wordcloud = WordCloud(stopwords=wordcloudStopWords).generate(userText)


    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(
        os.path.join(fileDirectory, user if user else "None" + ".png"),
        dpi=900)
    plt.close('all')




