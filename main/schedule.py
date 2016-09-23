#!/usr/bin/env python3

from requests.exceptions import HTTPError
import time, sys
from math import floor
from datetime import datetime as dt
from web_scrape.mp_scrape import multi_req
from web_scrape.scrape_csv import get_page


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
        try:
            if abs(cur_time - dt.now().minute) % int_time in range(0, tol):
                multi_req(urls)
                time.sleep(int_time*60)
            else:
                time.sleep(60)
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

def result_filter(**kwargs): #FIXME: implement filters: in analyze.py
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
    subs = ['https://reddit.com/r/'+sub for sub in args]
    sub_name = [i for i in args]
    for i in reversed(range(len(subs))):
        try:
            get_page(subs[i])
        except HTTPError:
            del subs[i]
            del sub_name[i]
    if not subs:
        print(
              "All subreddits entered were invalid. Please make "
              "sure that the subreddits entered actually exist and "
              "try again."
              )
        sys.exit(0)

    try:
        int_time = kwargs['int_time']
        tol = kwargs['tol']
    except KeyError:
        int_time = 20
        tol = None
    print('Currently scheduled {0} for every {1} min \n'
          'Please use ctrl-C to exit'.format(sub_name, int_time))
    sched_request(subs, int_time, tol)


if __name__ == "__main__":
    read_subs(
            'all', 'indieheads', 'hiphopheads', 'programming',
            'python', 'garbage_garbage_garbage_garbage_garbage'
            )

