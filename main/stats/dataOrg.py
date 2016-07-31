#!/usr/bin/python

# Should RedditEntry.dtFormat be a global variable? Probably...


from datetime import datetime
from time import mktime
import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import matplotlib.colors as colors
import re

from RddtPrs import RedditEntry as Entry
from RddtPrs import Article

def Getdata():
    Data = Entry.load("data.json")

    EntryList = []

    k = 0
    for i in Data:
        for j in range(len(Data[i])):
            Ent = Entry()
            Ent.parse(i, Data[i][j])
            EntryList.append(Ent)

    EntryList.sort(key=lambda x: x.date)

    for i in EntryList:
        toDel = []
        if len(i.articles) > 25:
            for j in range(len(i.articles)):
                if i.articles[j].rank == -1:
                    toDel.append(j)
            for k in toDel:
                i.articles.pop(k)
    return EntryList

def clean(Data, sub=0):
    Dates = np.array([i.date for i in Data[sub::4]])
    AllVotes = np.array([i.articles[0].votes for i in Data[sub::4]])

    toDel = []
    for i in range(len(AllVotes)):
        if not AllVotes[i]:
            toDel.append(i)

    Dates =  dt.date2num(np.delete(Dates, toDel))
    AllVotes = np.delete(AllVotes, toDel)
    return (Dates, AllVotes)

def VotesTime(Data, name):
    f, AX = plt.subplots(2, 2, sharex='col', sharey='row')
    for sub in range(4):
        Dates, AllVotes = clean(Data, sub)
        AX[int(sub/2)][sub%2].plot_date(Dates, AllVotes, fmt='ro', xdate=True)
        AX[int(sub/2)][sub%2].plot_date(Dates, AllVotes, fmt='k', xdate=True)
        AX[int(sub/2)][sub%2].xaxis_date()


    plt.savefig('{}.png'.format(name))
    plt.show()

def ArticleTrack(Data, sub, name, vr, begin=0, end=10000):
    Sub = Data[sub::4]

    trackDict = {}
    for entryNum in range(len(Sub)):
        for article in Sub[entryNum].articles:
            if article in Sub[entryNum-1].articles:
                trackDict[article.title].append(article)
            else:
                trackDict[article.title] = [article]

    artData = []

    for key in trackDict:
        artData.append([key,[(i, getattr(trackDict[key][i], vr)) for i in range(len(trackDict[key]))]])


    for article in artData:
        if article[1][-1][0] < begin:    # To decrease number analyzed
            continue                   # Only include those on page for >300h
        if article[1][-1][0] > end:
            continue
        instance = [inst[0] for inst in article[1]]
        vote = [vot[1] for vot in article[1]]

        toDel = None
        if vr == 'rank':
            for i in range(len(vote)):
                if vote[i] == 25:
                    toDel = i+1
                    break
        vote = np.array(vote[:toDel])
        instance = np.array(instance[:toDel])
        if vote.any():
#        plt.plot(instance, vote, 'ro')
            plt.plot(instance, vote, 'k')
            plt.plot(instance[-1], vote[-1], 'ro')

    plt.savefig('{0}{1}VSTimeOnfrontpage.png'.format(name, vr))

def Weigh(Data, sub=0, NoArt=True):
    WordDic = {}
    for All in Data[sub::4]:
        for art in All.articles:
            if not art.votes:
                continue
            words = list(filter(bool, re.split('\W+', art.title)))
            words = list(filter(lambda x: x not in ('', ',', ',,'), words))
            words = list(filter(lambda x: x not in ('quot', 's'), words))
            if NoArt:
                words = list(filter(lambda x: x not in ('the', 'a', 'to',
                    'of', 'in', 'I', 'is', 'quot', 'for', 'you', 'and',
                    'or', 'on', 'my', 'The', 'was', 'it', 'this', 'This',
                    'from', 'are', 'at', 'just', 'A', 'his', 'me', 'an',
                    'that', 'My', 't', 'by', 'with', 'When', 'have', 'be'),
                                                                        words))

            total = art.votes
            avg = total/len(words)

            for i in range(len(words)):
                try:
                    WordDic[words[i]] += avg
                except KeyError:
                    WordDic[words[i]] = avg
                    pass

    WordList = [(WordDic[i],i) for i in sorted(WordDic, key=WordDic.get, reverse=True)]
    return WordList

def Graph(data, name):
    data = np.array(data)
    plt.bar(range(len(data)),
                data[:,0].astype(np.float))
    plt.xticks(range(len(data)), data[:,1])

    plt.savefig("{0}.png".format(name))


if __name__ == "__main__":
    OrgData = Getdata()
    namelist = ["All","AllTop", "Indie", "HHH"]
    restricts = [35,0,0,0]

    for i in range(4):
        ArticleTrack(OrgData, i, namelist[i], vr='votes', begin=restricts[i])
        ArticleTrack(OrgData, i, namelist[i], vr='rank', begin=restricts[i])
