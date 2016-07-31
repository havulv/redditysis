#!/usr/bin/python

#Switching to urlib2 from lxml because lxml is shit for some reason.

import os
import time
import re
import csv
import requests
from BeautifulSoup import BeautifulSoup


SearchPages = [ ("http://www.reddit.com/r/all", 'all', {}), ("http://www.reddit.com/r/all/top", 'all/top', {}), ("http://www.reddit.com/r/indieheads", 'indieheads', {}), ("http://www.reddit.com/r/hiphopheads", 'hiphopheads', {})]


def get_page_data(url):
    end_tag = re.compile('[^/]+(?=/$|$)')
    fname = end_tag.match(url)
    hdr = {'User-Agent' : 'Looking for content by /u/Sea_Wulf'}
    page_data = []

    req = requests.get(url, params=hdr)
    if req.status_code != 200:
        raise HTTPError

    soup = BeautifulSoup(req.text)
    Content = soup.find("div", {"id":"siteTable"})

    for row in Content:
        rank = row.find('span', {"class": "rank"})
        vote = row.find('div', {"class": "midcol unvoted"})
        articles = row.find('div', {"class": "entry unvoted"})
        if articles == None:
            pass
        else:
            item = articles.find('p', {"class" : "title"})
            page_data.append(int(rank.string),
            int(vote.find('div', {"class" : "score unvoted"}).string),
            item.find('a').string,
            item.find('a').get('href'),
            item.find('span', {"class": "domain"}).find('a').get('href'))

    fpath = os.path.join(os.path.dirname(os.gecwd()), 'Redd_data')
    f_name = os.path.join(fpath,fname+"_data.json")
    head = re.compile("(Rank)")
    with open(f_name, "rb") as check_head:
        first = check_line.readline()

    save = csv.writer(open(f_name, "ab"))
    if not head.match(first):
        save.writerow(["Rank", "Votes", "Title", "Link",
    save.write("\n"+time.asctime()+"\n")
    save.write(json.dumps(SearchPages))


