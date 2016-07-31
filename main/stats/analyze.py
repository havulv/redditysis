#!/usr/bin/python3

import csv
from linear_analysis.py import *
import numpy as np

def words_list(words):
    ''' Args: string Returns: regex list of words in string '''
    reg = re.compile("\W+")
    return list(filter(lambda x: x is not "", reg.split(words)))

def read_csv(fname):
    '''
        Takes in a subreddit filename that has been scraped and returns
        7 lists of the data
        Args:                   Parameter
            fname       str(subreddit name)
        Returns:
            times               list
            ranks               list
            votes               list
            titles              list
            links               list
            domains             list
    '''
    fpath = os.path.join(os.path.dirname(os.getcwd()), 'Redd_data')
    fname = os.path.join(fpath, fname+"_data.csv")

    red_file = open(fname, 'rb')
    red_csv = csv.reader(red_file)
    times = [row[0] for row in red_csv]
    ranks = [row[1] for row in red_csv]
    votes = [row[2] for row in red_csv]
    titles = [row[3] for row in red_csv]
    links = [row[5] for row in red_csv]
    domains = [row[6] for row in red_csv]
    red_file.close()

    return times, ranks, votes, titles, links, domains

