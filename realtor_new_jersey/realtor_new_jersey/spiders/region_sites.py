# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from time import sleep
import random

class RegionSitesSpider(scrapy.Spider):
    name = 'region_sites'
    allowed_domains = ['realtor.com']
    #start_urls = ['http://realtor.com/local/New-Jersey/']

    def parse(self, response):
        region_boxes = response.xpath("//div[@id='top-cities']/table/tbody/tr")
        region_dict = {}

        for region in region_boxes:
            region_name = region.xpath(".//td[@class='col-area']/a/text()").extract_first()
            region_url = region.xpath(".//td[@class='text-center']/a/@href").extract_first()
            region_full_url = response.urljoin(region_url) + "?pgsz=50"
            region_dict[region_name] = region_full_url

        yield region_dict
