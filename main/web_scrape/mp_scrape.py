#!/usr/bin/env python3

import sys

from requests.exceptions import HTTPError
import logging
from .scrape_csv import get_page_data
import multiprocessing as mp

logging.basicConfig(
        filename="redditscrape.log",
        format="[%(levelname)s];[%(name)s] -- %(asctime)s: %(message)s")


def multi_req(urls):
    with mp.Pool(processes=len(urls)) as pool:
        try:
            pool.map(get_page_data, urls)
        except HTTPError as e:
            logging.debug("Error in retrieving data: {}".format(e))
    return


if __name__ == "__main__":
    subs = sys.argv[1:]
    if subs:
        subs = list(filter(lambda x: "reddit.com/" in x, subs))
        multi_req(subs)

