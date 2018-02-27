# -*- coding: utf-8 -*-

import scrapy
#from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from time import sleep
import random

import logging
from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging, _get_handler

import csv

with open('region_urls.csv') as f:
    reader = csv.reader(f)
    region_names = next(reader)
    region_urls = next(reader)

@defer.inlineCallbacks
def crawl():

    s = get_project_settings()

    the_counter = 0

    for i in range(0,25):
        csvout_name = "_".join(region_names[i].split()) + ".csv"
        s.set('FEED_FORMAT', 'csv')
        s.set('FEED_URI', csvout_name)


        configure_logging(settings=s, install_root_handler=False)
        logging.root.setLevel(logging.NOTSET)
        handler = _get_handler(s)
        logging.root.addHandler(handler)

        runner = CrawlerRunner(s)
        yield runner.crawl('berkeley', start_urls=[region_urls[i]], delay_counter = the_counter)

        logging.root.removeHandler(handler)

        the_counter  = the_counter + 1

    reactor.stop()

crawl()
reactor.run()
