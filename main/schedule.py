#!/usr/bin/python

import time
from math import floor
from datetime import datetime as dt
from web_scrape.mp_scrape import multi_req



def sched_request(urls, int_time=20, tol=None):
    '''
        Schedule get requests to [urls] to occur every int_time
        Args:                   Parameters
             urls           list(subreddits)
             int_time=20    int(time interval (min))
             tol=None       int(time tolerance (min))
                default: max(floor(0.25*int_time),1)
    '''
    cur_time = dt.now().minute
    if not tol:
        tol = .25*int_time
        tol = floor(tol) if floor(tol) > 0 else 1
    while True:
        if abs(cur_time - dt.now().minute) % int_time in range(0, tol):
            multi_req(urls)
            time.sleep(int_time*60)
        else:
            time.sleep(60)

def result_filter(**kwargs):
    '''
        Filter the results of each sched_result into a certain format.
        Called following sched_request so as to not interfer with write
        priveleges.
        Args:               Key             Entry
            **kwargs
    '''
def read_subs(*args,**kwargs):
    '''
        Take in a list of subreddits and options to query
        Args:                   Parameters:
             *args          arg[i] = str(subreddit name)
             **kwargs       int_time=20
                            tol=None
    '''

