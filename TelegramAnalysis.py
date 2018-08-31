import json
import os
import datetime
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab


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

dates = {}
dates2 = []

# "date": "2016-01-09T10:26:04",

for message in messages:

    if message["type"] == "message":

        if message['from'] not in users.keys():
            users[message["from"]] = 0

        else:
            users[message["from"]] += 1

        dateDict = convertTime(message["date"])
        date = dateDict["date"]

        if date not in dates.keys():
            dates[date] = []
        dates[date].append(message)



userTotals = {}

formatString = ""
for user in users.keys():
    userTotals[user] = []


for date in sorted(dates.keys()):

    tempValue = {}
    for user in users.keys():
        tempValue[user] = 0

    for message in dates[date]:
        tempValue[message["from"]] += 1

    for user in users.keys():
        userTotals[user].append(tempValue[user])


overallPlotData = {}

for user in userTotals:

    plotData = []

    overallSum = 0
    for entry in userTotals[user]:
        overallSum += int(entry)
        plotData.append(overallSum)

    overallPlotData[user] = plotData

    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(len(plotData)), plotData, '-', linewidth=1.5, label='Theoretical')


    plt.savefig(
        os.path.join(user if user else "None" + ".png"),
        dpi=150)
    plt.close('all')
    """


fig, ax = plt.subplots(figsize=(8, 4))
for user in overallPlotData.keys():
    ax.plot(range(len(overallPlotData[user])), overallPlotData[user], '-', linewidth=1.5, label=user)

ax.legend()

plt.savefig(
    os.path.join("overall.png"),
    dpi=150)
plt.close('all')










print(users)





