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
import logging as log
import os, re, csv, time, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

log.basicConfig(
        level=log.DEBUG,
        filename="redditscrape.log",
        format="[%(levelname)s];[%(name)s] -- %(asctime)s: %(message)s"
        )

def get_page(url):
    '''
        Get url for a subreddit
        Args:                   Parameter
             url        str(https://reddit.com/r/{subreddit})
        Returns:
             req.text           html
    '''
    u_agent = {
        'User-Agent' : ('Data sampling :: '
        'github.com/jandersen7/redditysis (by /u/Sea_Wulf)')
        }
    log.info("Sending Get Request to {}".format(url))
    req = requests.get(url, headers=u_agent)

    timeout = 0
    while req.status_code == 429 and timeout <= 60:
        log.info("Rate limit hit. Waiting 15 seconds and trying again")
        time.sleep(15)
        req = requests.get(url)
        timeout += 15
    if timeout > 60:
        log.debug("Request limit hit. Timed out after 60 seconds")
        sys.exit(0)
    elif req.status_code != 200:
        log.debug("Fatal error in querying: Status {0}; URL: {1}".format(
                                                            req.status_code,
                                                            url
                                                            ))
        raise requests.exceptions.HTTPError
    log.info("Status Code 200")
    return req.text

def get_tags(row):
    '''
        Clean html for data
        Args:                   Parameter
             row            Beautiful Soup tag element
        Returns:
             data               list(data)
    '''
    word_split = re.compile('\W+')
    try:
        date = row.find_all('time')[0].attrs['datetime']
        date = date[:len(date)-3]+date[-2:]
        timestamp = dt.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        votes = int(row.find_all(
                'div',
                {'class' : 'score unvoted'}
                )[0].string)
        author = row.attrs['data-author']
        subreddit = row.attrs['data-subreddit']
        rank = int(row.attrs['data-rank'])
        data_type = row.attrs['data-type']
        data_domain = row.attrs['data-domain']
        a_attrs = row.find_all('a')
        if a_attrs[0].string == None:
            a_attrs[0] = a_attrs[1]
        title = '\"' + a_attrs[0].string + '\"'    '''
        Get url for a subreddit
        Args:                   Parameter
             url        str(https://reddit.com/r/{subreddit})
    '''
        comments = int(word_split.split(a_attrs[-2].string)[0])
        return [
            timestamp, votes, author, subreddit, rank,
            data_type, data_domain, title, comments,
            ]
    except KeyError:
        log.info("Hit upon a row without any data {0}")
        pass

def save_csv(fname, page_data):
    '''
        Save data to a csv of filename fname_data.csv
        Args:                   Parameter
             fname              str(fname)
             page_data      list(list(data))
        Returns:
             None
    '''
    fpath = os.path.join(os.path.dirname(os.getcwd()), 'Redd_data')
    f_name = os.path.join(fpath,fname+"_data.csv")
    head = re.compile("(Rank)")
    log.info("Checking for existing header in file")
    first = ""
    try:
        with open(f_name, "r", encoding="utf-8") as check_head:
            first = check_head.readline()
    except FileNotFoundError:
        n_file = open(f_name, "w+")
        n_file.close()

    log.info("--- Writing to file ---")
    to_save = open(f_name, "a", encoding='utf-8', newline='')
    save = csv.writer(to_save)
    if not head.search(first):
        log.info("Writing Header")
        save.writerow([
            "Time", "Votes", "Author", "Subreddit", "Rank",
            "Data Type", "Domain", "Title", "Comments"
            ])
    save.writerows(page_data)
    to_save.close()
    log.info("--- Closing File ---")

def get_page_data(url):
    '''
        Retrieve page_data from a reddit subreddit url. If anything
        other than a 200 code, raises HTTPError. Saves the resulting
        data within a file named after the subreddit in Redd_data
        EX: ({subreddit}_data.csv)
        Args:  arg          param
               url     str(subreddit url)
    '''
    soup = BeautifulSoup(get_page(url), "html.parser")
    Content = soup.find("div", {"id":"siteTable"})

    page_data = []
    for row in Content:
        if row['class'][0] not in ['clearleft', 'nav-buttons']:
            page_data.append(get_tags(row))

    end_tag = re.compile('[^/]+(?=/$|$)')
    fname = end_tag.search(url).group(0)
    save_csv(fname, page_data)
