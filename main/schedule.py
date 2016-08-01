#!/usr/bin/python

import time
from datetime import datetime as dt
from web_scrape.mp_scrape import multi_req



def sched_request(urls, int_time=20):
    cur_time = dt.now().minute
    while True
        if abs(cur_time - dt.now().minute) % int_time in range(0,6):
            multi_req(urls)
            time.sleep(int_time*60)
        else:
            time.sleep(60)
