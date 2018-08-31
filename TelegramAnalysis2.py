import json
import os
import datetime
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from emoji_parse import EmojiDict


def convertTime(timestring):

    # 2016-01-09T10:26:04

    timeList = timestring.split("T")

    day = timeList[0].split("-")
    minute = timeList[1].split(":")

    date = datetime.date(year=int(day[0]), month=int(day[1]), day=int(day[2]))
    time = datetime.time(hour=int(minute[0]), minute=int(minute[1]), second=int(minute[2]))

    return {"date": date, "time": time}







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



emojiDict = {}
with open("data/emoji_table.txt", encoding="utf-8") as emojiFile:

    for line in emojiFile:
        line = line.replace("\n", "")
        emojiDict[line] = 0



formatString = ""
for user in users.keys():

    userDict = emojiDict.copy()

    rawData = userTexts[user]

    for text in rawData:

        for emoji in userDict.keys():
            if emoji in text:
                userDict[emoji] += 1

        #if '\U0001f600' in text:
        #    print("Match")
        #    print('\U0001f600')
        #userDict.add_emoji_count(text)


    overallCount = 0
    for key in userDict.keys():
        #print(key + ":" + str(userDict[key]))
        overallCount += int(userDict[key])

    print(user)
    print(str(overallCount))
    #print(userDict.dict_total)




