#!/usr/bin/env python3

try:
    from .linear_analysis import *
except ImportError:
    pass
import re, csv, os
import numpy as np

def words_list(words):
    ''' Args: string Returns: regex list of words in string '''
    return list(filter(lambda x: x is not "", re.split('\W+',words)))

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

    red_file = open(fname, 'r', newline='')
    red_csv = csv.reader(red_file, delimiter=",")
    red_csv.__next__()
    times = [row[0] for row in red_csv]
    ranks = [row[1] for row in red_csv]
    votes = [row[2] for row in red_csv]
    titles = [row[3] for row in red_csv]
    links = [row[5] for row in red_csv]
    domains = [row[6] for row in red_csv]
    red_file.close()

    return times, ranks, votes, titles, links, domains

def percent_from_avg(val_list):
    ''' Returns the percentage distance from the avg for each value '''
    return [(1-(i/(sum(val_list)/len(val_list)))) for i in val_list]

def domain_filter(domains, dom_filter):
    ''' Filters for dom_filter based on a list of domains/users/subreddit'''
    return [1 if dom == dom_filter else 0 for dom in domains]


def str_relation_matrix(titles, votes, ranks):
    ''' lasso algorithm on string length and votes (failed--revamp)'''
    raw_data = np.array([
        [len(words_list(i)) for i in titles],
        [int(i) for i in votes],
        [int(i) for i in ranks]
        ])
    W = np.array(center(raw_data))
    W = W.T
    xSelect = [True]*W.shape[1]
    xSelect[2] = False
    X = np.array(W[:, np.array(xSelect)])
    Y = np.array(W[:, np.array([not i for i in xSelect])])
    TMax = lasso_step(X,Y)
    TMax = 2000 if TMax < 20 else TMax
    PlotAndExplain(X,Y, np.int(TMax), "title length and such")
    return True

def main_testing():
    ''' main function (Still testing the kinks) '''
    time, rank, vote, title, link, domain = read_csv('all')
    if str_relation_matrix(title, vote, rank):
        print("Lasso successful")

if __name__ == "__main__":
    main_testing()
