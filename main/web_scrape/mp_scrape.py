#!/usr/bin/python3

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
            logging.debug("Error in retrieving data:{}".format(e))
    return



