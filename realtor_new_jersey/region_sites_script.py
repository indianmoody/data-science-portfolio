# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
settings.set('FEED_FORMAT', 'csv')
settings.set('FEED_URI', 'region_urls.csv')

process = CrawlerProcess(settings)

process.crawl('region_sites', start_urls=['https://realtor.com/local/New-Jersey/'])

process.start()
