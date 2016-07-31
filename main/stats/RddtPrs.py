#!/usr/bin/python

from time import mktime
from datetime import datetime
import ast

class RedditEntry(object):

    def __init__(self):
        self.reddit = u""
        self.cat = u""
        self.date = datetime.today()
        self.dtFormat = "%a %b %d %H:%M:%S %Y"
        self.articles = []

    def __repr__(self):
        return self.cat

    def __str__(self):
        return "{0}-{1} {2}".format(datetime.strftime(self.date, self.dtFormat), self.cat, len(self.articles))

    def load(data, length=0, dtFormat = "%a %b %d %H:%M:%S %Y"):
        with open(data, "r+") as GetData:
            AllLines = GetData.readlines()
            if not length:
                DatNData = AllLines
            else:
                DatNData = AllLines[0:(2*length)]

        DataDict = {}

        for i in filter(lambda x : not x%2, range(len(DatNData))):

            DataDict[datetime.strptime(DatNData[i].rstrip(), dtFormat)] = ast.literal_eval(DatNData[i+1].rstrip())

        return DataDict

    def parse(self, Date, DataEntry):
        self.reddit = DataEntry[0]
        self.cat = DataEntry[1]
        self.date = Date
        ArtDict = DataEntry[2]
        for i in ArtDict:
            self.articles.append(Article(i, ArtDict[i][0], ArtDict[i][1], ArtDict[i][2], ArtDict[i][3]))

        self.order()

    def order(self):
        if not not list:
            self.articles.sort(key=lambda x: x.rank)



class Article(object):

    def __init__(self, rank, votes, title, link, domain):
        self.title = title
        try:
            self.rank = int(rank)
        except ValueError:
            self.rank = -1
        self.link = link
        self.domain = domain
        try:
            self.votes = int(votes)
        except ValueError:
            self.votes = 0
            pass
    def __repr__(self):
        return "{0}".format(self.title)

    def __str__(self):
        return "Rank:{0}\nTitle:{1}\nVotes:{2}".format(self.rank, self.title, self.votes)

    def __eq__(self, other):
        if self.title == other.title and self.link == other.link and self.domain == other.domain:
            return True
        else:
            return False

if __name__ == "__main__":
    M = RedditEntry()
    Data = M.load("data.json")
    j = 0
    for i in Data:
        for j in range(len(Data[i])):
            M.parse(i,Data[i][j])
            break
        break

