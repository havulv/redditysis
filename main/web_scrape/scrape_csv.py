#!/usr/bin/python

'''
    Short module for saving reddit data as a csv.
    Consider moving to mp_scrape because the file length is small and
    there is only only one function.

    TO DO:
        logging
        unittesting
        updated documentation
'''

import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

SearchPages = [ ("http://www.reddit.com/r/all", 'all', {}), ("http://www.reddit.com/r/all/top", 'all/top', {}), ("http://www.reddit.com/r/indieheads", 'indieheads', {}), ("http://www.reddit.com/r/hiphopheads", 'hiphopheads', {})]


def get_page_data(url):
    '''
        Retrieve page_data from a reddit subreddit url. If anything
        other than a 200 code, raises HTTPError. Saves the resulting
        data within a file named after the subreddit in Redd_data
        EX: ({subreddit}_data.csv)
        Args:  arg          param
               url     str(subreddit url)
    '''
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
            page_data.append((
            dt.utcnow(),
            int(rank.string),
            int(vote.find('div', {"class" : "score unvoted"}).string),
            '\"'+item.find('a').string+'\"',
            '\"'+item.find('a').get('href')+'\"',
            '\"'+item.find('span',
                {"class": "domain"}).find('a').get('href') +'\"'
            ))

    fpath = os.path.join(os.path.dirname(os.getcwd()), 'Redd_data')
    f_name = os.path.join(fpath,fname+"_data.csv")
    head = re.compile("(Rank)")
    with open(f_name, "rb") as check_head:
        first = check_line.readline()

    to_save = open(f_name, "ab")
    save = csv.writer(to_save)
    if not head.match(first):
        save.writerow(["Time", "Rank", "Votes", "Title", "Link", "Domain"])
    save.writerows(page_data)
    to_save.close()
