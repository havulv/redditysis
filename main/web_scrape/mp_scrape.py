#!/usr/bin/python3


import logging
from scrape2json.py import get_page_data
import multiprocessing as mp

logging.basicConfig(filename="redditscrape.log", format="[%(levelname)s];[%(name)s] -- %(asctime)s: %(message)s")


def multi_req(urls):
    with mp.Pool as pool:
        try:
            pool.map(get_page_data, urls)
        except HTTPError as e:
            logging.info("Error in retrieving data:{}".format(e))
    return



